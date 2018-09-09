# coding: utf-8

from lang import helpers
from .BaseCommand import BaseCommand


class InstallCommand(BaseCommand):
    """
    Installs the i18n basic configuration and resources

    lang:install
        {--m|mock : Mocks the filesystem for testing}
    """

    def trigger(self):

        self.create_language("default", title="Default")
        self.create_config_resources()

        return self.end()

    def create_config_resources(self):

        path = "/config"

        fs_config = helpers.open_or_make_dir(self.fs_app, path)

        filename = "language.py"

        path = "/snippets/configs/" + filename

        if self.copy_file_from_package_to_fs(filename, path, fs_config):
            self.quiet or self.info("Installed /config/language.py")
        else:
            self.quiet or self.info("/config/language.py already exists")

        fs_config.close()
