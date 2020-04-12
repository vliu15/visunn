#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains node class to contain all metadata passed to frontend '''

from tensorboard.compat.proto.node_def_pb2 import NodeDef
from google.protobuf.json_format import MessageToDict

__all__ = ['Node']


class Node(object):
    def __init__(self, meta):
        if isinstance(meta, NodeDef):
            meta = MessageToDict(meta)

        assert isinstance(meta, dict)

        # NOTE: the metadata is stored in __dict__ (should attributes be
        # useful in compatibility with protobuf format)
        # #####################################################################
        # mandatory fields
        self.name = meta['name']
        self.op = meta['op']

        # optional fields
        self.input = meta.get('input', [])
        self.attr = meta.get('attr', {})

    def addattr(self, name, value):
        ''' add attributes to the node '''
        if name not in ['output', 'coords', 'type']:
            print('WARNING: {} is an unsupported attribute.'.format(name))
        if name in self._meta.keys():
            print('WARNING: overwriting the {} attribute.'.format(name))

        self.__dict__[name] = value

    def export(self):
        ''' return node metadata in json-friendly format '''
        return self.__dict__
