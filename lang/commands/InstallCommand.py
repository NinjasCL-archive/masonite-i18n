# coding: utf-8

from cleo import Command
from fs import open_fs
from fs.copy import copy_file

from lang import package_directory


class InstallCommand(Command):
    '''
    Installs the i18n basic configuration and resources

    install:lang
        {--m|mock : Mocks the filesystem for testing}
    '''

    def handle(self):
        self.trigger(self.option('mock'), self.option('verbose'))

    def trigger(self, mock = False, silent = True):

        command = self.init(mock, silent)

        command.create_lang_resources()
        command.create_config_resources()

        command.fs_pkg.close()

        return command.fs_app

    def init(self, mock = False, silent = True):
        # fs_opener tells which filesystem to use
        # See https://docs.pyfilesystem.org/en/latest/openers.html
        # We will use the current dir in the operating system fs as default value

        fs_opener = 'osfs://.'

        if mock:
            silent or self.info('Mock mode activated. Using memory filesystem.')
            fs_opener = 'mem://'

        fs_app = open_fs(fs_opener)
        fs_pkg = open_fs(package_directory)

        return self.init_with_fs(fs_app, fs_pkg, mock, silent)

    def init_with_fs(self, fs_app, fs_pkg, mock = False, silent = True):

        self.fs_app = fs_app
        self.fs_pkg = fs_pkg
        self.mock = mock
        self.silent = silent

        return self

    def create_lang_resources(self):

        path = '/resources/lang/default/'

        if not self.fs_app.exists(path):
            fs_lang = self.fs_app.makedirs(path)
        else:
            fs_lang = self.fs_app.opendir(path)

        if fs_lang.isempty('.'):

            filename = '__init__.py'

            copy_file(
                src_fs = self.fs_pkg,
                src_path = '/snippets/resources/lang/default/' + filename,
                dst_fs = fs_lang,
                dst_path = filename
            )

            self.silent or self.info('Installed /resources/lang/default')
        else:
            self.silent or self.info('/resources/lang/default already exists')

        fs_lang.close()

    def create_config_resources(self):

        path = '/config'

        if not self.fs_app.exists(path):
            fs_config = self.fs_app.makedirs(path)
        else:
            fs_config = self.fs_app.opendir(path)

        filename = 'locale.py'

        if not fs_config.isfile(filename):

            copy_file(
                src_fs = self.fs_pkg,
                src_path = '/snippets/configs/' + filename,
                dst_fs = fs_config,
                dst_path = filename
            )

            self.silent or self.info('Installed /config/locale.py')
        else:
            self.silent or self.info('/config/locale.py already exists')

        fs_config.close()
