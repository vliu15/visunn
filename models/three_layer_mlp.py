#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains simple mlp for image classification '''

from torch import nn

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['ThreeLayerMLP']


class ThreeLayerMLP(nn.Module):
    ''' simple fully-connected model for image classification '''
    def __init__(self, num_classes=10, **kwargs):
        super().__init__(**kwargs)
        layers = [
            nn.Flatten(1, -1),
            nn.Linear(32*32*3, 1024, bias=True),
            nn.ReLU(inplace=True),
            nn.Linear(1024, 256, bias=True),
            nn.ReLU(inplace=True),
            nn.Linear(256, num_classes, bias=True),
        ]
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)
