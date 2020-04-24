#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains basic utilities for graphing '''

import networkx as nx
import numpy as np

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['plot']


def _rescale_to_gaussian(xs, ys, v=7.5):
    xmean = np.mean(xs)
    xstd = np.std(xs)
    if xstd < 1e-3:
        def xnorm(x): return 0
    else:
        def xnorm(x): return (x - xmean) / xstd * v

    ymean = np.mean(ys)
    ystd = np.std(ys)
    if ystd < 1e-3:
        def ynorm(y): return 0
    else:
        def ynorm(y): return (y - ymean) / ystd * v

    return xnorm, ynorm


def plot(edges, normalize=True, truncate=False):
    ''' plots the graph and retrieves coordinates

        edges      (dict) : mapping of each node to its inputs
        normalize  (bool) : whether to normalize coordinates
        truncate   (bool) : whether to truncate names of nodes
                                      (useful when rendering with graphviz)
    '''
    # [1] first create graph by adding edges
    # #########################################################################
    G = nx.DiGraph()
    for name, inputs in edges.items():
        for in_name in inputs:
            G.add_edge(in_name, name)

    # [2] truncate names for visibility (for debugging purposes)
    # #########################################################################
    if truncate:
        G = nx.relabel.relabel_nodes(G, lambda x: '/'.join(x.split('/')[-3:]))

    # [3] get the actual coordinates from the dot algorithm
    # #########################################################################
    pos = nx.nx_pydot.graphviz_layout(G, prog='dot')

    # [4] normalize values for displaying on canvas
    # #########################################################################
    # a couple of options (still experimenting):
    #   [a] rescale coordinates to uniform distribution
    #   [b] rescale coordinates to normal distribution
    #
    # also allow user to specify the center and spread of the distributions
    # #########################################################################

    xs, ys = zip(*pos.values())
    xnorm, ynorm = _rescale_to_gaussian(
        list(set(xs)), list(set(ys)), v=len(edges)
    )

    for node, (x, y) in pos.items():
        pos[node] = (xnorm(x), ynorm(y))

    return G, pos
