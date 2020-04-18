#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' script for backend debugging and sanity checks '''

import os
import time
import argparse
from pprint import pprint
from pympler import asizeof
import networkx as nx
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.utils.tensorboard._pytorch_graph import graph

from models import torch_models
from constants import DATA_DIR
from visuai.plot import plot
from visuai.util import proto_to_dict, process_nodes, process_modules, \
                        build_modu

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

    # [1] convert model to protobuf
    start = time.time()
    graphdef, _ = graph(model, inputs)
    end = time.time()
    print('[1] convert model to protobuf: {:.3f}s'
          .format(end - start), flush=True)
    print('    protobuf footprint: {}b'
          .format(graphdef.ByteSize()), flush=True)

    # [2] convert protobuf to dict
    start = time.time()
    graphdict = proto_to_dict(graphdef)
    end = time.time()
    print('[2] convert protobuf to dict: {:.3f}s'
          .format(end - start), flush=True)
    print('    dict footprint: {}b'
          .format(asizeof.asizeof(graphdict)))

    # [3] prune trivial nodes
    start = time.time()
    graphdict = process_nodes(graphdict)
    end = time.time()
    print('[3] prune trivial nodes: {:.3f}s'
          .format(end - start), flush=True)
    print('    dict footprint: {}b'
          .format(asizeof.asizeof(graphdict)))

    # [4] prune trivial modules
    start = time.time()
    graphdict = process_modules(graphdict)
    end = time.time()
    print('[4] prune trivial modules: {:.3f}s'
          .format(end - start), flush=True)
    print('    dict footprint: {}b'
          .format(asizeof.asizeof(graphdict)))

    # [5] build modularized topology
    start = time.time()
    modu = build_modu(graphdict)
    end = time.time()
    print('[5] build modularized topology: {:.3f}s'
          .format(end - start), flush=True)
    print('    modu footprint: {}b'
          .format(asizeof.asizeof(modu)))

    # [6] interactive plotting
    if args.shell:
        pprint(list(modu.modules))
        while True:
            module = input('Select a module from the list above: ')

            # [a] export module metadata
            start = time.time()
            meta, inputs, outputs = modu.export(module)
            end = time.time()
            print('  [a] export module metadata: {:.3f}s'
                  .format(end - start))
            print('      metadata footprint: {}b'
                  .format(asizeof.asizeof((meta, inputs, outputs))))

            # [b] create all edges
            start = time.time()
            edges = {}
            for name, node in meta.items():
                if 'input' in list(node):
                    edges[name] = [
                        in_name for in_name in node['input']if in_name in meta
                    ]
            end = time.time()
            print('  [b] create all edges: {:.3f}s'
                  .format(end - start))
            print('      edges footprint: {}b'
                  .format(asizeof.asizeof(edges)))

            # [c] get node coordinates
            start = time.time()
            G, coords = plot(edges, normalize=True, truncate=False)
            end = time.time()
            print('  [c] get node coords: {:.3f}s'
                  .format(end - start))
            print('      coords footprint: {}b'
                  .format(asizeof.asizeof(coords)))

            # [d] (n/a to web app) render plt topology
            start = time.time()
            plt.figure(figsize=(8, 8))
            nx.draw(
                G, coords,
                node_size=100, node_color='gray', font_size=8,
                font_weight='light', with_labels=True
            )
            end = time.time()
            print('  [d] (n/a to web app) render plt topology: {:.3f}s'
                  .format(end - start))
            print('      plt topology footprint: {}b'
                  .format(asizeof.asizeof(plt)))

            plt.show()
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, default='ThreeLayerMLP',
                        help='string of callable (torchvision) model')
    parser.add_argument('-s', '--shell', default=False, action='store_true',
                        help='whether to run interactive shell mode')
    args = parser.parse_args()

    # uncomment to erase ApplePersistenceIgnoreState warning (only need once)
    # #########################################################################
    # import subprocess
    # subprocess.run([
    #     'defaults',
    #     'write',
    #     'org.python.python',
    #     'ApplePersistenceIgnoreState',
    #     'NO'
    # ])
    # #########################################################################

    main(args)