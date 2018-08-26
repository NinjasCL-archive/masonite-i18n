# coding: utf-8
from cleo import Application, CommandTester
from the import expect

from lang.commands.InstallCommand import InstallCommand


class TestInstallCommand:

    def setup_method(self):

        self.locale = '/config/locale.py'
        self.lang = '/resources/lang/default/__init__.py'

    @staticmethod
    def run():

        install = InstallCommand()
        return install.mock_handle()

    def test_that_locale_file_was_installed(self):

        result = self.run()
        expect(result.isfile(self.locale)).to.be.true

    def test_that_lang_file_was_installed(self):

        result = self.run()
        expect(result.isfile(self.lang)).to.be.true

    def test_that_locale_file_is_not_empty(self):

        result = self.run()
        contents = result.gettext(self.locale)
        expect(contents).to.be.a(str)
        expect(contents).NOT.be.empty

    def test_that_lang_file_is_not_empty(self):

        result = self.run()
        contents = result.gettext(self.lang)
        expect(contents).to.be.a(str)
        expect(contents).NOT.be.empty

    def test_that_command_works(self):

        application = Application()
        application.add(InstallCommand())

        command = application.find('install:lang')
        tester = CommandTester(command)

        result = tester.execute([
            ('command', command.get_name()),
            ('--mock')
        ])

        expect(result).to.be.an(int)
        expect(result).to.be(0)

        output = tester.get_display()

        expect(output).to.match('Mock mode activated')
        expect(output).to.match('Installed /resources/lang/default')
        expect(output).to.match('Installed /config/locale.py')
