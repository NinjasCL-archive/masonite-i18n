# coding: utf-8

from fs.copy import copy_fs, copy_structure

from lang.helpers.filesystem import load

# See
# https://docs.pyfilesystem.org/en/latest/reference/copy.html?highlight=copy_structure#fs.copy.copy_fs # noqa, flake8 issue


def root(walker=None):

    base = load.root()
    mock = load.mock()

    copy_fs(base, mock, walker=walker)
    base.close()

    return mock


def root_only_structure(walker=None):

    base = load.root()
    mock = load.mock()

    copy_structure(base, mock, walker=walker)
    base.close()

    return mock
