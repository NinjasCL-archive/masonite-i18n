# coding: utf-8

from fs import open_fs

from lang import package_directory

# See https://docs.pyfilesystem.org/en/latest/openers.html


def os(path='.'):
    # We will use the current dir in the operating system fs as default value
    return open_fs('osfs://' + path)


def mock():
    return open_fs('mem://')


def package():
    return open_fs(package_directory)
