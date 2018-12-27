#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = '1.2.0'

REQUIREMENTS = [
    "pillow >= 3.3.1"
]

with open("readme.rst", 'r') as f:
    long_description = f.read()

setup(
    name="colorgram.py",
    version=VERSION,
    install_requires=REQUIREMENTS,
    packages=['colorgram'],
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)
