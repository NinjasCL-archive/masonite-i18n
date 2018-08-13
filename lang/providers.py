# -*- coding: utf-8 -*-
""" A Language Locale Service Provider """

from masonite.provider import ServiceProvider
from lang.commands.InstallCommand import InstallCommand

class LangProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('LangInstallCommand', InstallCommand())

    def boot(self):
        pass
