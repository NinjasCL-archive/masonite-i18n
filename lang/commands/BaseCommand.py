# coding: utf-8

from cleo import Command

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
            self.quiet or self.info('Mock mode activated. Using memory filesystem.')
            fs_app = filesystem.load.mock()

        self.fs_app = fs_app
        self.fs_pkg = filesystem.load.package()

        return self.trigger()

    def handle(self):
        self.mock = self.option('mock')
        self.quiet = self.option('verbose')

        return self.init()

    def handle_mock(self, quiet=True):
        self.mock = True
        self.quiet = quiet

        return self.init()

    def create_language(self, name, title):
        create_lang_dir(self, name=name, title=title)

    def trigger(self):
        raise NotImplementedError()
