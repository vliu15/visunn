#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains simple convnet for cifar image classification '''

from torch import nn

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['ThreeLayerConvNet']


class ThreeLayerConvNet(nn.Module):
    ''' simple convolutional neural network for image classification '''
    def __init__(self, num_classes=10, **kwargs):
        super().__init__(**kwargs)
        layers = [
            nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1, bias=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(16, 8, kernel_size=3, stride=2, padding=1, bias=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(8, 4, kernel_size=3, stride=2, padding=1, bias=True),
            nn.Flatten(1, -1),
            nn.Linear(64, num_classes, bias=True)
        ]
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)
