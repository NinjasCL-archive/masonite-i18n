# coding: utf-8
"""A Language Locale Service Provider."""

from masonite.provider import ServiceProvider

from lang.commands.AddCommand import AddCommand
from lang.commands.InstallCommand import InstallCommand
from lang.commands.LangCommand import LangCommand
from lang.commands.NewCommand import NewCommand


class LangProvider(ServiceProvider):
    """
    Binds package classes to Masonite.

    Tells which commands, middleware and other related files
    must be loaded when installing masonite-i18n package.

    See
    https://docs.masoniteproject.com/v/v2.1/architectural-concepts/service-providers
    """

    """
    The wsgi = False just tells Masonite that this specific provider
    does not need the WSGI server to be running.
    """
    wsgi = False

    def register(self):
        """Execute the registration of package components to Masonite ecosystem.

        When the server is booted, Masonite will execute all
        register methods on all service providers.
        """
        self.app.bind("LangInstallCommand", InstallCommand())
        self.app.bind("LangNewCommand", NewCommand())
        self.app.bind("LangAddCommand", AddCommand())
        self.app.bind("LangCommand", LangCommand())

    def boot(self):
        """Execute logic after registration.

        This Method will have access to everything that is registered in the container.
        Is actually resolved by the container.
        """
        pass
