# coding: utf-8

from fs import open_fs

from lang import package_directory
from lang.helpers.filesystem import openers, paths


def os(path='.'):
    # We will use the current dir in the operating system fs as default value
    return open_fs(openers.OPERATING_SYSTEM + path)


def mock():
    return open_fs(openers.MEMORY)


def fs(opener):
    return open_fs(opener)


def root():
    return os(paths.ROOT)


def package():
    return os(package_directory)
