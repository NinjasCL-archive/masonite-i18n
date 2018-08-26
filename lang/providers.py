# coding: utf-8
""" A Language Locale Service Provider """

from masonite.provider import ServiceProvider

from lang.commands.InstallCommand import InstallCommand
from lang.commands.NewCommand import NewCommand


class LangProvider(ServiceProvider):

    wsgi = False

    def register(self):

        self.app.bind('LangInstallCommand', InstallCommand())
        self.app.bind('LangNewCommand', NewCommand())

    def boot(self):
        pass
