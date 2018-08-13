import pytest
from masonite.app import app
from lang.commands.InstallCommand import InstallCommand

class TestInstallCommand:

    def setup_method(self):
        self.app = App()
