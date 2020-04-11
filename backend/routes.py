#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains blueprint routing for flask app '''

from copy import deepcopy
from pprint import pprint
from flask import Blueprint, jsonify, request
from google.protobuf.json_format import MessageToDict

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
        if tag == 'root':
            module = modu.root
        else:
            module = tag.replace(';', '/')

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

    # [2] create mapping from node to nodedef (json compatible)
    # #####################################################################
    meta = {node.name: MessageToDict(node) for node in proto.node}

    # [3] get node positions (mapping, name:{x,y})
    # #####################################################################
    _, coords = plot(proto, normalize=True, truncate=False)

    # [4] get edges (mapping, node:input) and input/output nodes
    # #####################################################################
    nodes_and_outputs = set()
    nodes_and_inputs = set()
    edges = {}
    for node in proto.node:
        edges[node.name] = [name for name in node.input]
        nodes_and_inputs.update(edges[node.name])
        if len(node.input) > 0:
            nodes_and_outputs.add(node.name)

    # outputs is set difference { nodes_and_outputs - nodes_and_inputs }
    outputs = list(nodes_and_outputs.difference(nodes_and_inputs))
    # inputs is set difference { nodes_and_inputs - nodes_and_outputs }
    inputs = list(nodes_and_inputs.difference(nodes_and_outputs))

    # [5] re-package in json-compatible format
    # #####################################################################
    # meta    : dict( name : node )
    # coords  : dict( name : (x,y) )
    # edges   : dict( name : [input] )
    # inputs  : set( inputs )
    # outputs : set( outputs )
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
