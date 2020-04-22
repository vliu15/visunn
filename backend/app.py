#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' contains flask app to serve the backend '''

import os
import pickle
from flask import Flask
from flask_cors import CORS

from constants import MODU_EXT
from backend.routes import topology_blueprint

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'

__all__ = ['App']


class App(object):
    def __init__(self, logdir, name):
        self._app = Flask(__name__)
        CORS(self._app)
        self._app.config.update(dict(debug=True))

        # load model topology
        with open(os.path.join(logdir, name + MODU_EXT), 'rb') as f:
            self._modu = pickle.load(f)

        # register blueprint routings
        self._app.register_blueprint(
            topology_blueprint(self._modu), url_prefix='/topology'
        )

    def run(self):
        self._app.run()
