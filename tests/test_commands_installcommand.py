# coding: utf-8

from the import expect

from lang.commands.InstallCommand import InstallCommand


class TestInstallCommand:

    def setup_method(self):

        self.fsurl = 'mem://'
        self.locale = '/config/locale.py'
        self.lang = '/resources/lang/default/__init__.py'

    def run(self):

        install = InstallCommand()
        return install.handle(self.fsurl)

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
