#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' console script for visunn module '''

import argparse
from gevent.pywsgi import WSGIServer

from visunn.backend.app import App

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'


def run_main():
    ''' entry point for console script '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logdir', type=str, required=True,
                        help='string corresponding to saved model')
    parser.add_argument('-n', '--name', type=str, required=True,
                        help='string of model name')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='port number to launch web app on')
    args = parser.parse_args()

    app = App(args.logdir, args.name).app
    server = WSGIServer(('localhost', args.port), app)

    format_name = '\033[92m' + 'visunn ' + '\033[0m'
    print()
    print('\t' + format_name + 'deployed on http://localhost:{}'
          .format(args.port))
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt as ki:
        server.stop()
        print('\033[95m' + 'exited' + '\033[0m')


if __name__ == '__main__':
    run_main()
