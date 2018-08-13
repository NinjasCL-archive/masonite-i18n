# -*- coding: utf-8 -*-
""" A Language Locale Service Provider """

from masonite.provider import ServiceProvider
from lang.commands.LangInstallCommand import LangInstallCommand

class LangProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('LangInstallCommand', LangInstallCommand())

    def boot(self):
        pass
