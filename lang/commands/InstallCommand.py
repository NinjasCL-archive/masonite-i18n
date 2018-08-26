# coding: utf-8

from cleo import Command
from lang.helpers import filesystem
from fs.copy import copy_file


class InstallCommand(Command):
    """
    Installs the i18n basic configuration and resources

    install:lang
        {--m|mock : Mocks the filesystem for testing}
    """

    def __init__(self):
        super(InstallCommand, self).__init__()
        self.fs_app = None
        self.fs_pkg = None
        self.mock = True
        self.quiet = True

    def handle(self):
        self.trigger(self.option('mock'), self.option('verbose'))

    def mock_handle(self):
        return self.trigger(mock=True)

    def trigger(self, mock=False, quiet=True):

        command = self.init(mock, quiet)

        command.create_lang_resources()
        command.create_config_resources()

        command.fs_pkg.close()

        return command.fs_app

    def init(self, mock=False, quiet=True):

        fs_app = filesystem.get.os()

        if mock:
            quiet or self.info('Mock mode activated. Using memory filesystem.')
            fs_app = filesystem.get.mock()

        fs_pkg = filesystem.get.package()

        return self.init_with_fs(fs_app, fs_pkg, mock, quiet)

    def init_with_fs(self, fs_app, fs_pkg, mock=False, quiet=True):

        self.fs_app = fs_app
        self.fs_pkg = fs_pkg
        self.mock = mock
        self.quiet = quiet

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
                src_fs=self.fs_pkg,
                src_path='/snippets/resources/lang/default/' + filename,
                dst_fs=fs_lang,
                dst_path=filename
            )

            self.quiet or self.info('Installed /resources/lang/default')
        else:
            self.quiet or self.info('/resources/lang/default already exists')

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
                src_fs=self.fs_pkg,
                src_path='/snippets/configs/' + filename,
                dst_fs=fs_config,
                dst_path=filename
            )

            self.quiet or self.info('Installed /config/locale.py')
        else:
            self.quiet or self.info('/config/locale.py already exists')

        fs_config.close()
