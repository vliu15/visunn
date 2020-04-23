#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' script to start the backend server '''

import argparse

from visunn.backend.app import App

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logdir', type=str, required=True,
                        help='string corresponding to saved model')
    parser.add_argument('-n', '--name', type=str, required=True,
                        help='string of model name')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='port number to launch web app on')
    args = parser.parse_args()

    app = App(args.logdir, args.name).app
    app.run(use_reloader=True, port=args.port, threaded=True)
