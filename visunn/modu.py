#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains modu class for modular topology for backend api '''

from copy import deepcopy

from visunn.constants import MODU_ROOT

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
        self.add(self._root)

    @property
    def root(self):
        ''' retrieves root module of modular topology '''
        return self._root

    @property
    def modules(self):
        ''' retrieves names of all existing modules '''
        return self._modules.keys()

    def add(self, name):
        ''' initializes a new module '''
        self._modules[name] = {
            'modules': set(),
            'op_nodes': set(),
            'in_nodes': set(),
            'in_shapes': set(),
            'out_nodes': set(),
            'out_shapes': set(),
            'params': set()
        }

    def update(self, name, key, value):
        ''' updates the field of an existing module '''
        if name not in self.modules:
            self.add(name)
        self._modules[name][key].add(value)

    def export(self, name):
        ''' exports the metadata of the specified module as a dict '''
        module = self._modules[name]
        meta = {}

        def _fix_links(node):
            ''' edits node inputs to reflect modularization '''
            delim = len(node['input'])
            for idx, link in enumerate(node['input'] + node['output']):

                # if input comes from this module
                if link.find(name) == 0:
                    sub_name = link[len(name):].split('/')[0]

                    # if input comes from a submodule
                    if sub_name in module['modules']:
                        if idx < delim:
                            node['input'][idx] = name + sub_name + '/'
                        else:
                            node['output'][idx-delim] = name + sub_name + '/'

            # discard duplicates from multiple inputs from same module
            node['input'] = list(set(node['input']))
            node['output'] = list(set(node['output']))
            return node

        def _add_nodes(node_type):
            ''' adds nodes to the metadata dict '''
            for node_name in module[node_type]:
                # op_nodes only contain relative name
                if node_type == 'op_nodes':
                    node_name = name + node_name

                node = deepcopy(self._graphdict[node_name])

                # add input shapes (from input nodes' output shapes)
                if node_type == 'in_nodes':
                    node['input'] = []
                elif node_type == 'out_nodes':
                    node['output'] = []

                meta[node_name] = _fix_links(node)

        def _add_modules():
            ''' adds all modules to the metadata dict '''
            for submodule in module['modules']:
                sub_name = name + submodule + '/'
                submodule = self._modules[sub_name]

                node = {
                    'name': sub_name,
                    'op': 'visu::module',
                    'input': list(submodule['in_nodes']),
                    'output': list(submodule['out_nodes']),
                    'input_shapes': list(submodule['in_shapes']),
                    'output_shapes': list(submodule['out_shapes']),
                    'params': sorted(submodule['params'])
                }
                meta[sub_name] = _fix_links(node)

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
