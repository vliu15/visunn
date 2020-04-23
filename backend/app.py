#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains flask app to serve the backend '''

import os
import pickle
from flask import Flask, send_from_directory
from flask_cors import CORS

from constants import MODU_EXT
from backend.routes import api

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['App']


class App(object):
    def __init__(self, logdir, name, port):
        app = Flask(__name__, static_folder='../frontend/build')
        app.config.update(dict(debug=True))
        CORS(app)

        # load model topology
        with open(os.path.join(logdir, name + MODU_EXT), 'rb') as f:
            self._modu = pickle.load(f)

        # route build files
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve(path):
            if path != '' and os.path.exists(app.static_folder + '/' + path):
                return send_from_directory(app.static_folder, path)
            else:
                return send_from_directory(app.static_folder, 'index.html')

        # register blueprint routings
        app.register_blueprint(
            api(self._modu), url_prefix='/api'
        )

        self._port = port
        self._app = app

    def run(self):
        self._app.run(use_reloader=True, port=self._port, threaded=True)
