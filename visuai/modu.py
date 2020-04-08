#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains modu class for modular topology for backend api '''

from copy import deepcopy
from tensorboard.compat.proto.graph_pb2 import GraphDef
from tensorboard.compat.proto.node_def_pb2 import NodeDef
from tensorboard.compat.proto.versions_pb2 import VersionDef

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
        }

    def update_module(self, name, key, value):
        ''' updates the field of an existing module '''
        self._modules[name][key].add(value)

    def to_mod_proto(self, module):
        ''' exports specified module to protobuf format

            module   (str)  : full module name to convert to protobuf format
        '''
        # helper function
        # #####################################################################
        # checks each node input: inputs that come from submodules get mapped
        # to that submodule (to be consistent with modularlization)
        # #####################################################################
        def _fix_node_inputs(node):
            ''' edits node inputs to reflect modularization '''
            for idx, input_name in enumerate(node.input):
                # if input comes from this module
                if input_name.find(module) == 0:
                    sub_name = input_name[len(module):].split('/')[0]
                    # if input comes from a submodule
                    if sub_name in self._modules[module]['modules']:
                        node.input[idx] = module + sub_name + '/'
            return node

        # convert all modules and nodes to `NodeDef` proto
        # #####################################################################
        # sample function: node_proto()
        #   https://github.com/pytorch/...
        #       pytorch/blob/master/torch/utils/tensorboard/_proto_graph.py#L28
        #
        # all node names displayed in the module will be a relative path, since
        # the module specified will already be an absolute path
        #
        # input node names to this module (from other modules) will be full
        # paths, since their origin is from outside the module
        # #####################################################################
        list_of_nodes = []

        # [1] first deal with op_nodes (retrieve original proto and edit it)
        # #####################################################################
        for node_name in self._modules[module]['op_nodes']:
            full_name = module + node_name
            node = deepcopy(self._graphdict[full_name])
            node = _fix_node_inputs(node)

            list_of_nodes.append(node)

        # [2] then deal with modules (create new `NodeDef` proto for each one)
        # #####################################################################
        for submodule in self._modules[module]['modules']:
            name = module + submodule + '/'

            node = NodeDef(
                name=name.encode(encoding='utf-8'),
                op='visu::module',
                input=list(self._modules[name]['in_nodes']),
                attr={}
            )
            node = _fix_node_inputs(node)

            list_of_nodes.append(node)

        proto = GraphDef(node=list_of_nodes, versions=VersionDef(producer=22))
        return proto

    def to_flat_proto(self):
        ''' exports entire model, flattened, to protobuf format '''
        list_of_nodes = [node for node in self._graphdict.values()]
        proto = GraphDef(node=list_of_nodes, versions=VersionDef(producer=22))
        return proto
