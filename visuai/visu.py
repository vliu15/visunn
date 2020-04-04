#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains visu class for user api '''

import os
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from torch.utils.tensorboard._pytorch_graph import graph

from constants import LOG_DIR, MODU_FILE, MODU_ROOT
from visuai.plot import plot
from visuai.modu import Modu

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['Visu']


class Visu(object):
    ''' high level api for users '''
    def __init__(self, model, dataloader, logdir=''):
        ''' initializes visu, which builds model topology

            model       (torch.nn.Module)             : pytorch model
            dataloader  (torch.utils.data.Dataloader) : dataloader of inputs
            logdir      (str)                         : folder to dump pickle
        '''
        # [0] just get the first batch of inputs for now
        inputs, _ = next(iter(dataloader))

        # [1] use pytorch functionality to port to GraphDef proto
        # #####################################################################
        # `graph` function:
        #   https://github.com/pytorch/...
        #       pytorch/blob/master/torch/utils/tensorboard/_pytorch_graph.py
        #
        # `GraphDef` protobuf:
        #   https://github.com/tensorflow/...
        #       tensorflow/blob/master/tensorflow/core/framework/graph.proto
        #   from tensorboard.compat.proto.graph_pb2 import GraphDef
        #   fields: ['node', 'versions', 'version' (deprecated), 'library']
        #
        # `NodeDef` protobuf:
        #   https://github.com/tensorflow/...
        #       tensorflow/blob/master/tensorflow/core/framework/node_def.proto
        #   from tensorboard.compat.proto.node_def_pb2 import NodeDef
        #   fields: ['name', 'op', 'input', 'device', 'attr']
        #
        # consider adjusting code block here to get desired naming scheme
        #
        # NOTE: see note on recycled layers in README.md
        # #####################################################################
        graphdef, _ = graph(model, inputs)

        # [2] use bfs to prune nodes of op type 'prim'
        # #####################################################################
        # tensor basics:
        #   https://pytorch.org/cppdocs/notes/tensor_basics.html
        #
        # we only want to keep meaningful operations (that are directly relevant
        # to manipulating the input tensor), which is why we discard all
        # operations of type 'prim', which are non-tensor operations
        # #####################################################################
        graphdef = self._prune(graphdef)

        # [3] modularize pruned graph topology as a filesystem
        # #####################################################################
        # we want to retain the modularity of the topology so that it will be
        # easy to interact with and represent as a web app
        # #####################################################################
        self._modu = self._build(graphdef)

        # [4] log it for later access
        if logdir == '':
            logdir = 'test'
        logdir = os.path.join(LOG_DIR, logdir)
        # NOTE: uncomment to disallow collisions
        # #####################################################################
        # if os.path.exists(logdir) and os.path.isdir(logdir):
        #     raise OSError('The directory {} already exists.')
        # #####################################################################
        if os.path.exists(logdir):
            import shutil
            shutil.rmtree(logdir)
        os.makedirs(os.path.join(os.getcwd(), logdir))
        with open(os.path.join(logdir, MODU_FILE), 'wb') as f:
            pickle.dump(self._modu, f)

        # auxiliary functionality
        self._params = [name for name, _ in model.named_parameters()]
        self._logdir = logdir

    # TODO: write this function
    def update(self, iter, optim, loss):
        ''' logs updates to the model

            iter   (int)                   : iteration or epoch
            optim  (torch.optim.Optimizer) : pytorch optimizer
            loss   (torch.Tensor)          : tensor loss
        '''
        raise NotImplementedError

    def save(self, filename='topology.png'):
        ''' saves the topology to file '''
        # get coordinates of flattened graph from dot algorithm
        # #####################################################################
        # dot algorithm:
        #   https://www.graphviz.org/Documentation/TSE93.pdf
        # #####################################################################
        G, pos = plot(self._modu.to_flat_proto(),
                      normalize=False, truncate=True)
        plt.figure(figsize=(8, 8))
        nx.draw(
            G, pos,
            node_size=100, node_color='gray', font_size=8,
            font_weight='light', with_labels=True
        )
        plt.savefig(os.path.join(self._logdir, filename))

    @staticmethod
    def _build(graphdef):
        ''' builds the graph topology as a file system

            graphdef  (GraphDef.proto) : GraphDef proto of model
        '''
        md = Modu(graphdef, root=MODU_ROOT)

        # iterate through the nodes and add them to the tree
        for node in graphdef.node:
            modules = node.name.split('/')      # list of modules (directories)
            op_node = modules.pop(-1)           # node name (file)
            mod_name = md.root                  # to track module's absolute path

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

    @staticmethod
    def _prune(graphdef):
        ''' prunes non-tensor operations from graph topology

            graphdef  (GraphDef.proto) : GraphDef proto of model
        '''
        graphlist = list(graphdef.node)
        graphdict = {node.name: node for node in graphdef.node}
        queue = [graphlist[-1]]
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
                    # TODO: necessary to match param name with node name
                    continue
                # all other prim ops should be removed
                elif input_node.op.split('::')[0] == 'prim':
                    del_idxs.append(idx)
                    node.input.extend(input_node.input)
                    contains_prim = True
                # if input is still there, queue it
                elif input_name not in seen:
                    queue.append(input_node)

            # actually delete those inputs
            for idx in reversed(del_idxs):
                del node.input[idx]

            # if 'prim' inputs were removed, re-queue and re-evaluate
            if contains_prim:
                queue.append(node)

        # remove those nodes from the graph
        del_idxs = []
        for i in reversed(range(len(graphlist))):
            node = graphlist[i]
            if node.op.split('::')[0] == 'prim':
                del graphdef.node[i]

        return graphdef
