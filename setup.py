#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

from lang import version


setup(
    name='masonite-i18n',
    version=version,
    packages=[
        'lang',
        'lang.commands',
        'lang.helpers',
        'lang.middlewares'
    ],
    license='MIT',
    author='Camilo Castro',
    author_email='camilo@ninjas.cl',
    description='Provides i18n to Masonite',
    url='https://github.com/NinjasCL-labs/masonite-i18n',
    install_requires=[
        'hjson',
        'masonite',
        'cleo',
        'fs',
        'scandir'
    ],
    keywords=['i18n', 'translation', 'python3', 'masonite'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
