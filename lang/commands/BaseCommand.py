# coding: utf-8

from cleo import Command


class BaseCommand(Command):

    mock = False
    quiet = True

    def handle(self):
        self.mock = self.option('mock')
        self.quiet = self.option('verbose')

        return self.trigger()

    def handle_mock(self):
        self.mock = True
        return self.trigger()

    def trigger(self):
        raise NotImplementedError()
