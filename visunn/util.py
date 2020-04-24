#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains util functions to facilitate graph parsing '''

import re
from copy import copy
from google.protobuf.json_format import MessageToDict

from visunn.modu import Modu
from visunn.constants import MODU_ROOT

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['process_nodes', 'process_modules', 'build_modu', 'proto_to_dict']


def proto_to_dict(graphdef):
    ''' converts the graphdef protobuf to dict '''
    # some initialization
    _ = {
        'name': '',           # str         : node name
        'op': '',             # str         : op name
        'input': [],          # list(str)   : list of input names
        'output': [],         # list(str)   : list of output names
        'input_shapes': [],   # list(tuple) : list of input shape tuples
        'output_shapes': []   # list(tuple) : list of output shape tuples
    }

    graphdict = {}
    for node in graphdef.node:
        node = MessageToDict(node)
        graphdict[node['name']] = {
            'name': node.get('name', ''),
            'op': node.get('op', ''),
            'input': node.get('input', []),
            'output': [],
            'input_shapes': [],
            'output_shapes': []
        }
        if '_output_shapes' in node['attr']:
            shapes = node['attr']['_output_shapes']['list']['shape']
            for shape in shapes:
                if 'dim' in shapes:
                    graphdict[node['name']]['output_shapes'].append(
                        tuple(int(dim['size']) for dim in shape['dim'])
                    )

    return graphdict


def process_nodes(graphdict):
    ''' prunes non-tensor operations from graph topology

        graphdict  (dict) : mapping of node name to nodedict

        graphdict will serve as the master representation of the model topology
        and will reflect the removal of nodes in the pruning process
    '''
    # get list of output nodes
    outputs = set(graphdict.keys())
    for name, node in graphdict.items():
        outputs = outputs.difference(set(node['input']))

    # [1] prune nodes with bfs
    # #########################################################################
    queue = [copy(graphdict[name]) for name in outputs]
    seen = set()
    while len(queue) > 0:
        node = queue.pop(0)
        seen.add(node['name'])
        contains_prim = False

        del_idxs = []
        # for each input, merge its inputs if 'prim'
        for idx, input_name in enumerate(node['input']):
            input_node = graphdict.get(input_name, None)
            if input_node is not None:
                input_node = copy(input_node)

            # torch==1.4.0: delete nodes not in graphdef
            if input_node is None:
                del_idxs.append(idx)

            # bias and weight correspond to 'prim' ops, but should be kept
            elif input_name.split('/')[-2] in ['weight', 'bias']:
                # edit naming scheme (and metadata) of param nodes
                del graphdict[input_name]
                input_name = input_name.rsplit('/', 1)[0]
                graphdict[input_name] = {
                    'name': input_name,
                    'op': 'visu::param',
                    'input': [],
                    'output': [],
                    'input_shapes': [],
                    'output_shapes': input_node['output_shapes']
                }
                node['input'][idx] = input_name

            # all other prim ops should be removed
            elif input_node['op'].split('::')[0] == 'prim':
                del_idxs.append(idx)
                node['input'].extend(input_node['input'])
                contains_prim = True

            # if input is still there, queue it
            elif input_name not in seen:
                queue.append(copy(input_node))

        # delete inputs from node
        for idx in reversed(del_idxs):
            del node['input'][idx]

        # update node in graphdict
        graphdict[node['name']] = node

        # if 'prim' inputs were removed, re-queue and re-evaluate
        if contains_prim:
            queue.append(copy(node))

    # [2] clean up graphdict
    # #########################################################################
    for name in list(graphdict):
        node = graphdict[name]
        if node['op'].split('::')[0] == 'prim':
            graphdict.pop(name)

    # [3] add doubly linked connections with bfs
    # #########################################################################
    queue = [copy(graphdict[name]) for name in outputs]
    seen = set()
    while len(queue) > 0:
        node = queue.pop(0)
        name = node['name']
        seen.add(name)

        for in_name in node['input']:
            in_node = copy(graphdict[in_name])

            node['input_shapes'] += in_node['output_shapes']
            in_node['output'] += [node['name']]
            if in_name not in seen:
                queue.append(in_node)

        graphdict[name] = node

    return graphdict


def process_modules(graphdict):
    ''' collapses modules with only one module/node '''
    names = list(graphdict)

    # [1] accumulate submodules per module
    # #########################################################################
    # for each module, build track all submodules and nodes to identify which
    # modules are "trivial" and should be collapsed
    # #########################################################################
    contents = {}
    for name in names:
        mod_name = MODU_ROOT
        modules = name.split('/')
        op_node = modules.pop(-1)

        for module in modules:
            if mod_name in contents:
                contents[mod_name].add(module)
            else:
                contents[mod_name] = set([module])
            mod_name += module + '/'

        if mod_name in contents:
            contents[mod_name].add(op_node)
        else:
            contents[mod_name] = set([op_node])

    # [2] create mappings for pruned names
    # #########################################################################
    # accumulate all modules that only have 1 entry (and thus should be
    # collapsed), map them to the index of nested position so that names with
    # the module prefix can collapse the module at that position
    #
    # collapsing essentially merges the module with its child module/node by
    # removing the '/' and putting the module in parentheses so that the
    # modularizing code will not identify it as a module
    #
    # subtract 2 to get the index to accommodate for
    #   (1) len() is 1-indexed, and
    #   (2) modules end in '/', so len() over-counts by 1 position
    # #########################################################################
    prune_mods = set(
        (k, len(k.split('/'))-2) for k, v in contents.items() if len(v) <= 1
    )

    name_map = {}
    for name in names:
        map_idxs = set(idx for mod, idx in prune_mods if name.startswith(mod))
        if len(map_idxs) == 0:
            continue

        mapped_name = ''
        modules = name.split('/')
        op_node = modules.pop(-1)
        for idx, module in enumerate(modules):
            if idx not in map_idxs:
                mapped_name += module + '/'
            else:
                mapped_name += '(' + module + ')'
        name_map[name] = mapped_name + op_node

    # [3] apply mappings to all names
    # #########################################################################
    # edit all node names (inputs included) in the graphdict
    # NOTE: not sure if applying name changes here is the most efficient
    # #########################################################################
    for name in names:
        node = graphdict.pop(name)

        # update name if edited
        if name in name_map:
            name = name_map[name]
            node['name'] = name

        # update input names if edited
        for idx, in_node in enumerate(node['input']):
            if in_node in name_map:
                node['input'][idx] = name_map[in_node]

        # update node entry in graphdict
        graphdict[name] = node

    return graphdict


def build_modu(graphdict, params=None):
    ''' builds the graph topology as a file system

        graphdict  (dict) : mapping of node name to nodedict
        params     (list) : list of model parameter names (if specified, will
                            allow for association of param names to modules)
    '''
    md = Modu(graphdict, root=MODU_ROOT)

    # iterate through the nodes and add them to the tree
    for name, node in graphdict.items():
        modules = name.split('/')      # list of modules (directories)
        op_node = modules.pop(-1)      # node name (file)
        mod_name = md.root             # to track module's absolute path
        param_pattern = '.'.join(re.findall(r'\[(.*?)\]', name))

        # [1] add modules and param patterns
        # #####################################################################
        for module in modules:
            # add current module to previous module's list
            md.update(mod_name, 'modules', module)
            mod_name += module + '/'

            # add params if pattern matches
            if params is not None:
                if param_pattern + '.weight' in params:
                    md.update(mod_name, 'params', param_pattern + '.weight')
                if param_pattern + '.bias' in params:
                    md.update(mod_name, 'params', param_pattern + '.bias')

        # add op node to deepest nested module
        md.update(mod_name, 'op_nodes', op_node)

        # [2] add inputs/outputs to each module (comes from another module)
        # #####################################################################
        for in_name in node['input']:
            # grab output shapes
            in_node = graphdict[in_name]
            out_shapes = in_node['output_shapes']

            # prepare for modular linking
            in_modules = in_name.split('/')[:-1]
            in_mod_name = md.root
            out_mod_name = md.root

            # [2.1] first loop within the depth of both modules
            # #################################################################
            # the is_link parameter tracks when the first link occurs for that
            # module (since that must be when it is a link for all the
            # submodules)
            #
            # example of a link:
            #   node : a/b/c/d/e
            #   input: a/b/d/e/f
            #
            # a/b/d/e/f is an input to modules a/b/c/, a/b/c/d/ (vice versa for
            # outputs)
            # #################################################################
            is_link = False
            for idx in range(min(len(in_modules), len(modules))):
                out_module = modules[idx]
                in_module = in_modules[idx]
                out_mod_name += out_module + '/'
                in_mod_name += in_module + '/'

                if in_module != out_module or is_link:
                    # link inputs and outputs
                    md.update(out_mod_name, 'in_nodes', in_name)
                    md.update(in_mod_name, 'out_nodes', name)
                    is_link = True

                    # add input and output shapes
                    for out_shape in out_shapes:
                        md.update(out_mod_name, 'in_shapes', out_shape)
                        md.update(in_mod_name, 'out_shapes', out_shape)

            # [2.2] loop through the rest of the deeper output module
            # #################################################################
            # when the output module is deeper than the input module, it must
            # be that the input is a link to the output (and not vice versa)
            #
            # example of an input link:
            #   output: a/b/c/d/e
            #   input : a/b/c/
            #
            # a/b/c is an input to a/b/c/d/ and a/b/c/d/e (but those aren't
            # outputs to a/b/c, since they reside within a/b/c)
            # #################################################################
            if len(in_modules) < len(modules):
                for idx in range(len(in_modules), len(modules)):
                    out_mod_name += modules[idx] + '/'
                    md.update(out_mod_name, 'in_nodes', in_name)
                    for out_shape in out_shapes:
                        md.update(out_mod_name, 'in_shapes', out_shape)

            # [2.3] loop through rest of the deeper input module
            # #################################################################
            # when the input module is deeper than the output module, it must
            # be that the output is a link to the input (and not vice versa)
            #
            # example of an output link:
            #   output: a/b/c
            #   input : a/b/c/d/e
            #
            # a/b/c is an output to a/b/c/d/ and a/b/c/d/e (but those aren't
            # inputs to a/b/c, since they reside within a/b/c)
            # #################################################################
            elif len(in_modules) > len(modules):
                for idx in range(len(modules), len(in_modules)):
                    in_mod_name += in_modules[idx] + '/'
                    md.update(in_mod_name, 'out_nodes', name)
                    for out_shape in out_shapes:
                        md.update(in_mod_name, 'out_shapes', out_shape)

    return md
