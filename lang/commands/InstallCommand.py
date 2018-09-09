# coding: utf-8

from fs.copy import copy_file

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

        if not fs_config.isfile(filename):

            copy_file(
                src_fs=self.fs_pkg,
                src_path="/snippets/configs/" + filename,
                dst_fs=fs_config,
                dst_path=filename,
            )

            self.quiet or self.info("Installed /config/language.py")
        else:
            self.quiet or self.info("/config/language.py already exists")

        fs_config.close()
