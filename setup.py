#!/usr/bin/env python3
# coding: utf-8

from setuptools import find_packages, setup

from lang import name, version


setup(
    name=name,
    version=version,
    packages=find_packages(),
    license='MIT',
    author='Camilo Castro',
    author_email='camilo@ninjas.cl',
    description='Provides Basic i18n to Masonite',
    url='https://github.com/NinjasCL-labs/masonite-i18n',
    install_requires=[
        'hjson',
        'masonite',
        'cleo',
        'fs',
        'scandir',
        'jinja2'
    ],
    keywords=['i18n', 'translation', 'python3', 'masonite'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
