#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' script to start the backend server '''

import os
import argparse

from constants import LOG_DIR
from backend.app import App

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logdir', type=str, required=True,
                        help='string of callable (torchvision) model')
    args = parser.parse_args()

    logdir = os.path.join(LOG_DIR, args.logdir)
    app = App(logdir)
    app.run()
