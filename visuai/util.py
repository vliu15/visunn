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

__all__ = ['link_outputs', 'prune_nodes', 'build_modu']


class Node(object):
    def __init__(self, nodedef):
        self.__dict__.update(MessageToDict(nodedef))
        self.output = []


def link_outputs(graphdict):
    ''' adds output nodes to NodeDef '''
    # convert protobuf to class as dict
    for name in graphdict.keys():
        nodedef = graphdict.pop(name)
        graphdict[name] = Node(nodedef)

    # add output nodes
    for name, node in graphdict.items():
        for input_name in node.input:
            try:
                input_node = graphdict[input_name]
            except KeyError:
                print('WARNING: {} is not in the graphdict.')

            input_node.output.append(name)

    return graphdict


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
    del_names = set()
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
                del_names.add(input_name)
            # bias and weight correspond to 'prim' ops, but should be kept
            elif input_name.split('/')[-2] in ['weight', 'bias']:
                # TODO: necessary to match param name with node name
                continue
            # all other prim ops should be removed
            elif input_node.op.split('::')[0] == 'prim':
                del_idxs.append(idx)
                del_names.add(input_name)
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
    for name in del_names:
        graphdict.pop(name)

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

            if mod_name not in md.modules:
                md.add_module(mod_name)

        # add op node to nested module
        md.update_module(mod_name, 'op_nodes', op_node)

        # add inputs to each module (an input comes from another module)
        for in_node in node.input:
            in_modules = in_node.split('/')[:-1]
            mod_name = md.root

            is_input = False
            for idx in range(min(len(in_modules), len(modules))):
                module = modules[idx]
                in_module = in_modules[idx]
                mod_name += module + '/'
                if in_module != module or is_input:
                    md.update_module(mod_name, 'in_nodes', in_node)
                    is_input = True

            if len(in_modules) < len(modules):
                for idx in range(len(in_modules), len(modules)):
                    mod_name += modules[idx] + '/'
                    md.update_module(mod_name, 'in_nodes', in_node)

    return md