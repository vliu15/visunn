#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains blueprint routing for flask app '''

from copy import deepcopy
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

    @blueprint.route('/<tag>')
    def topology(tag):
        try:
            module = tag.split(';', 1)[1].replace(';', '/') + '/'
        except IndexError as ie:
            module = modu.root
        return get_topology(module, modu)

    return blueprint


def get_topology(module, modu):
    ''' returns the info needed to visualize module topology '''
    # [1] parse the route path
    # #####################################################################
    # following this format:
    #   root;module1;module2;...
    #
    # note that the incoming tag must have 'root' to represent the root
    # directory (as opposed to modu.root (default='')) since empty url
    # routing isn't as clear as explicitly labeling the root
    # #####################################################################
    proto = modu.to_mod_proto(module)

    # [2] get node positions (mapping, name:{x,y})
    # #####################################################################
    _, coords = plot(proto, normalize=True, truncate=False)

    # [3] get edges (mapping, node:input) and input/output nodes
    # #####################################################################
    nodes_and_outputs = set([node.name for node in proto.node])
    nodes_and_inputs = set()
    edges = {}
    for node in proto.node:
        edges[node.name] = [name for name in node.input]
        nodes_and_inputs.update(edges[node.name])

    # outputs is set difference { nodes_and_outputs - nodes_and_inputs }
    outputs = list(nodes_and_outputs.difference(nodes_and_inputs))

    # inputs is set difference { nodes_and_inputs - nodes_and_outputs }
    inputs = list(nodes_and_inputs.difference(nodes_and_outputs))

    # [3] re-package in json-compatible format
    # #####################################################################
    module = {
        'coords': coords,
        'edges': edges,
        'inputs': list(inputs),
        'outputs': list(outputs)
    }
    print(module)

    return jsonify(module)
