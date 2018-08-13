# -*- coding: utf-8 -*-
""" A lang Install Service Provider """

from masonite.provider import ServiceProvider
from lang.commands.InstallCommand import InstallCommand

class InstallProvider(ServiceProvider):

    wsgi = False

    def register(self):
        self.app.bind('LangInstallCommand', InstallCommand())

    def boot(self):
        pass
