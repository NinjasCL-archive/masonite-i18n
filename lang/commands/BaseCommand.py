# coding: utf-8

from cleo import Command
from fs.copy import copy_file

from lang.helpers import create_lang_dir, filesystem


class BaseCommand(Command):
    mock = None
    quiet = None
    fs_app = None
    fs_pkg = None

    def init(self):
        self.fs_app = None
        self.fs_pkg = None

        fs_app = filesystem.load.os()

        if self.mock:
            self.quiet or self.info("Mock mode activated. Using memory filesystem.")
            fs_app.close()
            fs_app = filesystem.load.mock()

        self.fs_app = fs_app
        self.fs_pkg = filesystem.load.package()

        return self.trigger()

    def end(self):
        self.fs_pkg.close()
        return self.fs_app

    def end_all(self):
        self.end()
        self.fs_app.close()

    def handle(self):
        self.mock = self.option("mock")
        self.quiet = self.option("verbose")

        return self.init()

    def handle_mock(self, quiet=True):
        self.mock = True
        self.quiet = quiet

        return self.init()

    def create_language(self, name, title):
        create_lang_dir(self, name=name, title=title)

    def copy_file_from_package_to_fs(self, filename, path, fs):
        if not fs.isfile(filename):

            copy_file(src_fs=self.fs_pkg, src_path=path, dst_fs=fs, dst_path=filename)

            return True
        return False

    def trigger(self):
        raise NotImplementedError()
