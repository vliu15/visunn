#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains util functions to facilitate graph parsing '''

from copy import copy
from tensorboard.compat.proto.node_def_pb2 import NodeDef
from google.protobuf.json_format import MessageToDict

from visuai.modu import Modu
from constants import MODU_ROOT

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['prune_nodes', 'prune_modules', 'build_modu']


def prune_nodes(graphdict):
    ''' prunes non-tensor operations from graph topology

        graphdict  (dict) : mapping of node name to NodeDef

        graphdict will serve as the master representation of the model topology
        and will reflect the removal of nodes in the pruning process
    '''
    # get list of output nodes
    outputs = set(graphdict.keys())
    for name, node in graphdict.items():
        outputs = outputs.difference(set(node.input))

    # initialize bfs
    queue = [graphdict[name] for name in outputs]
    seen = set()

    while len(queue) > 0:
        node = queue.pop(0)
        seen.add(node.name)
        contains_prim = False

        del_idxs = []
        # for each input, merge its inputs if 'prim'
        for idx, input_name in enumerate(node.input):
            input_node = graphdict.get(input_name, None)

            # torch==1.4.0: delete nodes not in graphdef
            if input_node is None:
                del_idxs.append(idx)

            # bias and weight correspond to 'prim' ops, but should be kept
            elif input_name.split('/')[-2] in ['weight', 'bias']:
                # edit naming scheme (and metadata) of weight nodes
                input_name = input_name.rsplit('/', 1)[0]
                input_node.op = 'visu::param'
                input_node.name = input_name
                del input_node.input[0]
                # update output node and logging
                node.input[idx] = input_name
                graphdict[input_name] = input_node

            # all other prim ops should be removed
            elif input_node.op.split('::')[0] == 'prim':
                del_idxs.append(idx)
                node.input.extend(input_node.input)
                contains_prim = True

            # if input is still there, queue it
            elif input_name not in seen:
                queue.append(copy(input_node))

        # delete inputs from node
        for idx in reversed(del_idxs):
            del node.input[idx]

        # update node in graphdict
        graphdict[node.name] = node

        # if 'prim' inputs were removed, re-queue and re-evaluate
        if contains_prim:
            queue.append(copy(node))

    # remove those nodes from the graphdict
    for name in list(graphdict):
        node = graphdict[name]
        if node.op.split('::')[0] == 'prim':
            graphdict.pop(name)

    return graphdict


def prune_modules(graphdict):
    ''' collapses modules that only contain one module or node '''
    names = list(graphdict)

    # [1] accumulate submodules per module
    # #########################################################################
    # for each module, build up all submodules and nodes
    # #########################################################################
    contents = {}
    for name in names:
        mod_name = MODU_ROOT
        modules = name.split('/')
        op_node = modules.pop(-1)

        for module in modules:
            if mod_name in contents.keys():
                contents[mod_name].add(module)
            else:
                contents[mod_name] = set([module])
            mod_name += module + '/'
        
        if mod_name in contents.keys():
            contents[mod_name].add(op_node)
        else:
            contents[mod_name] = set([op_node])

    # [2] created mappings for pruned names
    # #########################################################################
    # accumulate all modules that only have 1 entry (and thus should be
    # collapsed), map them to the index of nested position so that names with
    # the module prefix can delete the module at that position
    # #########################################################################
    prune_mods = set(
        (k, len(k.split('/'))-1) for k, v in contents.items() if len(v) <= 1
    )
    name_map = {}
    for name in names:
        del_idxs = set(idx for mod, idx in prune_mods if name.startswith(mod))
        pruned_name = name.split('/')

        for idx in sorted(del_idxs, reverse=True):
            del pruned_name[idx]
        name_map[name] = '/'.join(pruned_name)

    # [3] apply mappings to all names
    # #########################################################################
    # edit all node names (inputs included) in the graphdict
    # NOTE: not sure if applying name changes here is the most efficient
    # #########################################################################
    for name in list(graphdict):
        node = graphdict.pop(name)

        # update name if edited
        if name in name_map:
            name = name_map[name]
            node.name = name

        # update input names if edited
        for idx, in_node in enumerate(node.input):
            if in_node in name_map:
                node.input[idx] = name_map[in_node]

        # update node entry in graphdict
        graphdict[name] = node

    return graphdict


def build_modu(graphdict):
    ''' builds the graph topology as a file system

        graphdict  (dict) : mapping of node name to NodeDef
    '''
    md = Modu(graphdict, root=MODU_ROOT)

    # iterate through the nodes and add them to the tree
    for name, node in graphdict.items():
        modules = name.split('/')      # list of modules (directories)
        op_node = modules.pop(-1)      # node name (file)
        mod_name = md.root             # to track module's absolute path

        # add modules
        for module in modules:
            # add current module to previous module's list
            md.update_module(mod_name, 'modules', module)
            mod_name += module + '/'

            # initialize info for current module
            if mod_name not in md.modules:
                md.add_module(mod_name)

        # add op node to deepest nested module
        md.update_module(mod_name, 'op_nodes', op_node)

        # add inputs to each module (an input comes from another module)
        for in_node in node.input:
            in_modules = in_node.split('/')[:-1]
            in_mod_name = md.root
            out_mod_name = md.root

            is_link = False
            for idx in range(min(len(in_modules), len(modules))):
                out_module = modules[idx]
                in_module = in_modules[idx]
                out_mod_name += out_module + '/'
                in_mod_name += in_module + '/'

                if in_module != out_module or is_link:
                    md.update_module(out_mod_name, 'in_nodes', in_node)
                    md.update_module(in_mod_name, 'out_nodes', name)
                    is_link = True

            if len(in_modules) < len(modules):
                for idx in range(len(in_modules), len(modules)):
                    out_mod_name += modules[idx] + '/'
                    md.update_module(out_mod_name, 'in_nodes', in_node)
            elif len(in_modules) > len(modules):
                for idx in range(len(modules), len(in_modules)):
                    in_mod_name += in_modules[idx] + '/'
                    md.update_module(in_mod_name, 'out_nodes', name)

    return md