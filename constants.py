#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' some constants shared across backend python api's '''

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['DATA_DIR',
           'LOG_DIR', 'MODU_FILE',
           'MODU_ROOT',
           'NORM_FUNC', 'NORM_M', 'NORM_V']

# train config
DATA_DIR = 'data'

# visu config
LOG_DIR = 'logs'
MODU_FILE = 'modu.pt'

# modu config
MODU_ROOT = ''

# plot config
NORM_FUNC = '_rescale_to_uniform'
NORM_M = 0.0
NORM_V = 10.0
