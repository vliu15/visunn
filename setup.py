#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' visunn: aesthetic visualization of neural networks '''

from setuptools import setup, find_packages

__author__ = 'Vincent Liu'
__email__ = 'vliu15@stanford.edu'


README_md = ''
with open('README.md', 'r') as f:
    README_md = f.read()

REQUIRED_PACKAGES = [
    'torch>=1.4.0',
    'numpy>=1.15.1',
    'pydot>=1.4.1',
    'networkx>=2.4',
    'protobuf>=3.11.3',
    'flask>=1.1.1',
    'flask-cors>=3.0.8',
    'gevent>=20.4.0'
]

TEST_PACKAGES = [
    'matplotlib>=3.2.0',
    'pympler>=0.8',
    'torchvision>=0.5.0',
    'tqdm>=4.43.0',
    'scipy>=1.4.1'
]

CONSOLE_SCRIPTS = [
    'visu = visunn.main:run_main'
]

VERSION = '0.1.1'

setup(
    name='visunn',
    version=VERSION,
    author='Vincent Liu',
    author_email='vliu15@stanford.edu',
    description=__doc__,
    long_description=README_md,
    long_description_content_type='text/markdown',
    url='https://github.com/vliu15/visunn',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS
    },
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='MIT',
    python_requires='>=3.5',
    keywords='deep learning visualization neural networks pytorch torch'
)
