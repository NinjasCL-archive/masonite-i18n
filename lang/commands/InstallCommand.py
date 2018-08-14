# coding: utf-8

from cleo import Command
from fs import open_fs
from fs.copy import copy_file

from lang import package_directory


class InstallCommand(Command):
    '''
    Installs the i18n basic configuration and resources

    install:lang
    '''

    def handle(self, fsurl = 'osfs://.'):
        '''
        Handler

        Params:
            fsurl (string, optional) See https://docs.pyfilesystem.org/en/latest/openers.html
        '''

        fs_app = open_fs(fsurl)
        fs_pkg = open_fs(package_directory)

        path = '/resources/lang/default/'

        if not fs_app.exists(path):
            fs_lang = fs_app.makedirs(path)
        else:
            fs_lang = fs_app.opendir(path)

        if fs_lang.isempty('.'):

            filename = '__init__.py'

            copy_file(
                src_fs = fs_pkg,
                src_path = '/snippets/resources/lang/default/' + filename,
                dst_fs = fs_lang,
                dst_path = filename
            )

        fs_lang.close()

        path = '/config'

        if not fs_app.exists(path):
            fs_config = fs_app.makedirs(path)
        else:
            fs_config = fs_app.opendir(path)

        filename = 'locale.py'

        if not fs_config.isfile(filename):

            copy_file(
                src_fs = fs_pkg,
                src_path = '/snippets/configs/' + filename,
                dst_fs = fs_config,
                dst_path = filename
            )

            print('\033[92mDefault lang Configuration File Created!\033[0m')

        fs_config.close()
        fs_pkg.close()

        return fs_app
