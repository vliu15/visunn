#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains visu class for user api '''

import os
import pickle
from torch.utils.tensorboard._pytorch_graph import graph

from constants import LOG_DIR, MODU_FILE
from visuai.util import process_nodes, process_modules, build_modu
from visuai.modu import Modu

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['Visu']


class Visu(object):
    ''' high level api for users '''
    def __init__(self, model, dataloader, logdir='', name='model'):
        ''' initializes visu, which builds model topology

            model       (torch.nn.Module)             : pytorch model
            dataloader  (torch.utils.data.Dataloader) : dataloader of inputs
            logdir      (str)                         : folder to dump pickle
            name        (str)                         : model name, no real use
        '''
        pid = os.fork()

        # return parent process
        if pid != 0:
            return

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
        graphdict = {node.name: node for node in graphdef.node}

        # [2] use bfs to prune nodes of op type 'prim'
        # #####################################################################
        # tensor basics:
        #   https://pytorch.org/cppdocs/notes/tensor_basics.html
        #
        # we only want to keep meaningful operations (that are directly relevant
        # to manipulating the input tensor), which is why we discard all
        # operations of type 'prim', which are non-tensor operations
        # #####################################################################
        graphdict = process_nodes(graphdict)

        # [3] prune irrelevant modules that don't contribute to the hierarchy
        # #####################################################################
        # some modules only contain one submodule or one node, and such modules
        # are uninteresting and only complicate the hierarchical structure of
        # topology, so we collapse all modules that fall into this category
        graphdict = process_modules(graphdict)

        # [3] modularize pruned graph topology as a filesystem
        # #####################################################################
        # we want to retain the modularity of the topology so that it will be
        # easy to interact with and represent as a web app
        # #####################################################################
        self._modu = build_modu(graphdict)

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

        # terminate child process
        print('Successfully parsed and saved {} topology!'
              .format(name), flush=True)
        os._exit(0)

    # NOTE: see https://www.wandb.com for this functionality
    def update(self, iter, optim, loss):
        ''' logs updates to the model

            iter   (int)                   : iteration or epoch
            optim  (torch.optim.Optimizer) : pytorch optimizer
            loss   (torch.Tensor)          : tensor loss
        '''
        raise NotImplementedError
