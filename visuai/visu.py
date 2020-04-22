#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains visu class for user api '''

import os
import pickle
from torch.utils.tensorboard._pytorch_graph import graph

from constants import LOG_DIR, MODU_EXT
from visuai.util import proto_to_dict, process_nodes, process_modules, \
                        build_modu
from visuai.modu import Modu

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['Visu']


class Visu(object):
    ''' high level api for users '''
    def __init__(self, model, dataloader, logdir=LOG_DIR, name='model'):
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
        params = [name for name, _ in model.named_parameters()]

        # [1] use pytorch functionality to port to graphdef proto
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
        # NOTE: see note on recycled layers in README.md
        # #####################################################################
        graphdef, _ = graph(model, inputs)

        # [2] convert and parse graphdef proto to dict format
        # #####################################################################
        # this maps the name of a node to its relevant contents, saving space
        # and improving accessibility for downstream processing
        #
        # `NodeDef` protobuf:
        #   https://github.com/tensorflow/...
        #       tensorflow/blob/master/tensorflow/core/framework/node_def.proto
        #   from tensorboard.compat.proto.node_def_pb2 import NodeDef
        #   fields: ['name', 'op', 'input', 'device', 'attr']
        # #####################################################################
        graphdict = proto_to_dict(graphdef)

        # [3] use bfs to prune nodes of op type 'prim'
        # #####################################################################
        # tensor basics:
        #   https://pytorch.org/cppdocs/notes/tensor_basics.html
        #
        # we only want to keep meaningful operations (that are directly relevant
        # to manipulating the input tensor), which is why we discard all
        # operations of type 'prim', which are non-tensor operations
        # #####################################################################
        graphdict = process_nodes(graphdict)

        # [4] prune irrelevant modules that don't contribute to the hierarchy
        # #####################################################################
        # some modules only contain one submodule or one node, and such modules
        # are uninteresting and only complicate the hierarchical structure of
        # topology, so we collapse all modules that fall into this category
        # #####################################################################
        graphdict = process_modules(graphdict)

        # [5] modularize pruned graph topology as a filesystem
        # #####################################################################
        # we want to retain the modularity of the topology so that it will be
        # easy to interact with and represent as a web app
        # #####################################################################
        self._modu = build_modu(graphdict, params=params)

        # [6] log it for later access
        # #####################################################################
        # NOTE: uncomment to disallow collisions
        # if os.path.exists(logdir) and os.path.isdir(logdir):
        #     raise OSError('The directory {} already exists.')
        # #####################################################################
        if os.path.exists(logdir):
            import shutil
            shutil.rmtree(logdir)
        os.makedirs(os.path.join(os.getcwd(), logdir))
        with open(os.path.join(logdir, name + MODU_EXT), 'wb') as f:
            pickle.dump(self._modu, f)

        # terminate child process
        print('Successfully parsed and saved {} topology!'
              .format(name), flush=True)
        os._exit(0)

    # NOTE: see https://www.wandb.com for this intended functionality
    def update(self, iter, optim, loss):
        ''' logs updates to the model

            iter   (int)                   : iteration or epoch
            optim  (torch.optim.Optimizer) : pytorch optimizer
            loss   (torch.Tensor)          : tensor loss
        '''
        raise NotImplementedError
