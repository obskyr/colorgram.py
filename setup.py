#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup

VERSION = '1.3.0'

REQUIREMENTS = [
    "pillow >= 3.3.1"
]

with open("readme.rst", 'r') as f:
    long_description = f.read()


def get_packages(package):
    """ Return root package and all sub-packages. """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name="colorgram.py",
    version=VERSION,
    install_requires=REQUIREMENTS,
    packages=get_packages('colorgram'),
    package_data={'colorgram': ['colorgram/utils_c.pyx']},
    include_package_data=True,
    author="Samuel Messner",
    author_email="powpowd@gmail.com",
    url="https://github.com/obskyr/colorgram.py",
    download_url="https://github.com/obskyr/colorgram.py/tarball/v" + VERSION,
    description="A Python module for extracting colors from images. Get a palette of any picture!",
    long_description=long_description,
    license="MIT",
    keywords="color colors palette extract image picture",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
