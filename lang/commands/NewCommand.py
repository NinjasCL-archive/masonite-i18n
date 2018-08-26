# coding: utf-8
from cleo import Command
from fs import open_fs
from fs.copy import copy_file

from lang import package_directory


class NewCommand(Command):
    """
    Creates a new language with optional locale data

    new:lang
        {--m|mock : Mocks the filesystem for testing}
        {--l|locale : Locale identifier from localeplanet.com}
    """

    def handle(self):
        mock = self.option('mock')
        locale = self.option('locale')

        print(mock)
        print(locale)
