#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains blueprint routing for flask app '''

from copy import deepcopy
from pprint import pprint
from flask import Blueprint, jsonify

from visuai.plot import plot

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['topology_blueprint']


def topology_blueprint(modu):
    ''' creates routing for the topology feature

        modu  (Modu) : modu object
    '''
    blueprint = Blueprint('topology', __name__)

    @blueprint.route('/<tag>', methods=['GET'])
    def topology(tag):
        # [1] format the get request that comes in
        # #####################################################################
        if tag == 'root':
            module = modu.root
        else:
            module = tag.replace(';', '/')

        # [2] retrieve metadata from modu
        # #####################################################################
        meta, inputs, outputs = modu.export(module)

        # [3] accumulate edges between nodes
        # #####################################################################
        edges = {}
        for name, node in meta.items():
            if 'input' in list(node):
                edges[name] = list(node['input'])

        # [4] use these edges to plot and retrieve coordinates
        # #####################################################################
        _, coords = plot(edges, normalize=True, truncate=True)

        # [5] format and export as json
        # #####################################################################
        module = {
            'meta': meta,
            'coords': coords,
            'edges': edges,
            'inputs': inputs,
            'outputs': outputs
        }

        pprint(module)
        return jsonify(module)

    return blueprint
