import os
import shutil

from cleo import Command
from masonite.packages import create_or_append_config

package_directory = os.path.dirname(os.path.realpath(__file__))

class InstallCommand(Command):
    """
    Installs needed configuration lang files into a Masonite project
    ​
    lang:install
    """

    def handle(self):

        create_or_append_config(
            os.path.join(
                package_directory,
                '../../lang/snippets/configs/lang.py'
            )
        )

        # Create Resources
        directory = os.path.join(os.getcwd(), 'resources/lang/default/')
        lang = os.path.join(directory, '__init__.py')

        template = os.path.join(package_directory, '../../lang/snippets/resources/lang/default/__init__.py')

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isfile(lang):
            shutil.copyfile(template, lang)
            print('\033[92mDefault lang Configuration File Created!\033[0m')
