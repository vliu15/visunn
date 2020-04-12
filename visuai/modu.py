#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains modu class for modular topology for backend api '''

import json
from google.protobuf.json_format import MessageToDict

from constants import MODU_ROOT

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['Modu']


class Modu(object):
    ''' low level api for backend '''
    def __init__(self, graphdict, root=MODU_ROOT):
        self._graphdict = graphdict

        # initialize modules with root module
        self._root = root
        self._modules = {}
        self.add_module(self._root)

    @property
    def root(self):
        ''' retrieves root module of modular topology '''
        return self._root

    @property
    def modules(self):
        ''' retrieves names of all existing modules '''
        return self._modules.keys()

    def add_module(self, name):
        ''' initializes a new module '''
        self._modules[name] = {
            'modules': set(),
            'op_nodes': set(),
            'in_nodes': set(),
            'in_shapes': set(),
            'out_nodes': set(),
            'out_shapes': set()
        }

    def update_module(self, name, key, value):
        ''' updates the field of an existing module '''
        if name not in self.modules:
            self.add_module(name)
        self._modules[name][key].add(value)

    def export(self, name):
        ''' exports the metadata of the specified module as a dict '''
        module = self._modules[name]
        meta = {}

        def _fix_node_inputs(node):
            ''' edits node inputs to reflect modularization '''
            for idx, input_name in enumerate(node['input']):
                # if input comes from this module
                if input_name.find(name) == 0:
                    sub_name = input_name[len(name):].split('/')[0]
                    # if input comes from a submodule
                    if sub_name in module['modules']:
                        node['input'][idx] = name + sub_name + '/'
            return node

        def _add_nodes(node_type):
            ''' adds nodes to the metadata dict '''
            for node_name in module[node_type]:
                # op_nodes only contain relative name
                if node_type == 'op_nodes':
                    node_name = name + node_name

                node = MessageToDict(self._graphdict[node_name])
                node['input'] = node.get('input', [])
                node['attr'] = node.get('attr', {})

                # in_nodes are inputs to this module, so get rid of inputs
                if node_type != 'in_nodes':
                    for i, in_name in enumerate(node['input']):
                        in_node = MessageToDict(self._graphdict[in_name])
                        if '_output_shapes' in in_node['attr'].keys():
                            key_in = '_input_shapes_{}'.format(i)
                            key_out = '_output_shapes'
                            node['attr'][key_in] = in_node['attr'][key_out]
                    node = _fix_node_inputs(node)
                else:
                    node['input'] = []

                meta[node_name] = node

        def _add_modules():
            ''' adds all modules to the metadata dict '''
            for submodule in module['modules']:
                sub_name = name + submodule + '/'
                submodule = self._modules[sub_name]

                attr = {
                    '_output_shapes_{}'.format(i): json.loads(output_shape)
                    for i, output_shape in enumerate(submodule['out_shapes'])
                }
                attr.update({
                    '_input_shapes_{}'.format(i): json.loads(input_shape)
                    for i, input_shape in enumerate(submodule['in_shapes'])
                })

                node_info = {
                    'name': sub_name,
                    'op': 'visu::module',
                    'input': list(submodule['in_nodes']),
                    'output': list(submodule['out_nodes']),
                    'attr': attr
                }

                node = _fix_node_inputs(node_info)
                meta[sub_name] = node

        # convert all modules and nodes to dict
        # #####################################################################
        # all node names displayed in the module will be a relative path, since
        # the module specified will already be an absolute path
        #
        # input and output node names to this module (from other modules) will
        # be full paths, since their origin is from outside the module
        # #####################################################################
        _add_nodes('op_nodes')
        _add_nodes('in_nodes')
        _add_nodes('out_nodes')
        _add_modules()

        inputs = list(module['in_nodes'])
        outputs = list(module['out_nodes'])

        return (meta, inputs, outputs)
