#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains basic utilities for graphing '''

import networkx as nx
import numpy as np
from pprint import pprint

from constants import NORM_FUNC, NORM_M, NORM_V

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['plot']


def _rescale_to_uniform(xs, ys):
    xmax = max(xs)
    xmin = min(xs)
    xshift = (xmax - xmin) / 2.
    xscale = (xmax + xmin) / 2.
    if xshift < 1e-3:
        xnorm = lambda x: NORM_M
    else: 
        xnorm = lambda x: (x - xshift) / xscale * NORM_V + NORM_M

    ymax = max(ys)
    ymin = min(ys)
    yshift = (ymax - ymin) / 2.
    yscale = (ymax + ymin) / 2.
    if yshift < 1e-3:
        ynorm = lambda y: NORM_M
    else:
        ynorm = lambda y: (y - yshift) / yscale * NORM_V + NORM_M

    return xnorm, ynorm


def _rescale_to_gaussian(xs, ys):
    xmean = np.mean(xs)
    xstd = np.std(xs)
    if xstd < 1e-3:
        xnorm = lambda x: NORM_M
    else:
        xnorm = lambda x: (x - xmean) / xstd * NORM_V + NORM_M

    ymean = np.mean(ys)
    ystd = np.std(ys)
    if ystd < 1e-3:
        ynorm = lambda y: NORM_M
    else:
        ynorm = lambda y: (y - ymean) / ystd * NORM_V + NORM_M

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
    rescale_func = eval(NORM_FUNC)
    xnorm, ynorm = rescale_func(xs, ys)

    for node, (x, y) in pos.items():
        pos[node] = (xnorm(x), ynorm(y))

    return G, pos
