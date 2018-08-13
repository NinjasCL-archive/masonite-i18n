import os
from cleo import Command
from masonite.packages import create_or_append_config

package_directory = os.path.dirname(os.path.realpath(__file__))

class InstallCommand(Command):
    """
    Installs needed configuration locale files into a Masonite project
    ​
    locale:install
    """

    def handle(self):

        create_or_append_config(
            os.path.join(
                package_directory,
                '../locale/configs/locale.py'
            )
        )

        create_or_append_config(
            os.path.join(
                package_directory,
                '../locale/configs/application.py'
            )
        )