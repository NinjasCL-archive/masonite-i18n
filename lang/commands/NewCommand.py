# coding: utf-8
from cleo import Command
from fs import open_fs
from fs.copy import copy_file

from lang import package_directory


class NewCommand(Command):
    """
    Creates a new language with optional locale data

    lang:new
        {--m|mock : Mocks the filesystem for testing}
    """

    # def handle(self):
    #     mock = self.option('mock')
    #     print(mock)
