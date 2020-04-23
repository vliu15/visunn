#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains blueprint routing for flask app '''

from flask import Blueprint, jsonify

from visunn.plot import plot

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['api']


def api(modu):
    ''' creates routing for the topology feature

        modu  (Modu) : modu object
    '''
    blueprint = Blueprint('api', __name__)

    @blueprint.route('/<tag>', methods=['GET'])
    def topology(tag):
        # [1] format the get request that comes in
        # #####################################################################
        if tag == 'root':
            module = modu.root
        else:
            module = tag.replace(';', '/') + '/'

        # [2] retrieve metadata from modu
        # #####################################################################
        meta, inputs, outputs = modu.export(module)
        # revise inputs/outputs for root module
        if tag == 'root':
            inputs, outputs = [], []
            for name, node in meta.items():
                if len(node['input']) == 0:
                    inputs += [name]
                if len(node['output']) == 0:
                    outputs += [name]

        # [3] accumulate edges between nodes
        # #####################################################################
        edges = {}
        for name, node in meta.items():
            if 'input' in list(node):
                edges[name] = [
                    in_name for in_name in node['input'] if in_name in meta
                ]

        # [4] use these edges to plot and retrieve coordinates
        # #####################################################################
        _, coords = plot(edges, normalize=True, truncate=False)

        # [5] format and export as json
        # #####################################################################
        module = {
            'meta': meta,
            'coords': coords,
            'edges': edges,
            'inputs': inputs,
            'outputs': outputs
        }

        return jsonify(module)

    return blueprint
