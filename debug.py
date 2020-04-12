#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' script for backend debugging and sanity checks '''

import os
import time
import argparse
from pprint import pprint
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.utils.tensorboard._pytorch_graph import graph

from models import torch_models
from constants import DATA_DIR
from visuai.util import prune_nodes, prune_modules, build_modu

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'


def get_model_and_dataloader(name):
    # retrieve, initialize, & optionally load model
    model = torch_models.get(name, None)
    if model is None:
        print('Valid name specifications are {}'
                .format(', '.join(torch_models.keys())))
        raise RuntimeError
    else:
        model = model(num_classes=10)

    # set up dataloader
    download = False
    if not os.path.exists('cifar10'):
        os.makedirs('cifar10')
        download = True
    dataloader = DataLoader(
        datasets.CIFAR10(
            os.path.join(DATA_DIR, 'cifar10'),
            download=True,
            train=True,
            transform=transforms.ToTensor()
        ),
        batch_size=128,
        shuffle=True,
        drop_last=False
    )

    return model, dataloader


def main(args):
    model, dataloader = get_model_and_dataloader(args.name)

    inputs, _ = next(iter(dataloader))

    start = time.time()
    graphdef, _ = graph(model, inputs)
    end = time.time()
    print('[1] convert model to protobuf: {:.3f}s'
          .format(end - start), flush=True)

    start = time.time()
    graphdict = {node.name: node for node in graphdef.node}
    end = time.time()
    print('[2] convert protobuf to dict: {:.3f}s'
          .format(end - start), flush=True)

    start = time.time()
    graphdict = prune_nodes(graphdict)
    end = time.time()
    print('[3] prune trivial nodes: {:.3f}s'
          .format(end - start), flush=True)

    start = time.time()
    graphdict = prune_modules(graphdict)
    end = time.time()
    print('[4] prune trivial modules: {:.3f}s'
          .format(end - start), flush=True)

    start = time.time()
    modu = build_modu(graphdict)
    end = time.time()
    print('[5] build modularized topology: {:.3f}s'
          .format(end - start), flush=True)

    if args.shell:
        pprint(list(modu.modules))
        while True:
            module = input('Select a module from the list above: ')
            pprint(modu._modules[module])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, default='ThreeLayerMLP',
                        help='string of callable (torchvision) model')
    parser.add_argument('-s', '--shell', default=False, action='store_true',
                        help='whether to run interactive shell mode')
    args = parser.parse_args()
    main(args)