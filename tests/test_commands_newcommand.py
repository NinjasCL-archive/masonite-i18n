# coding: utf-8
from cleo import Application, CommandTester
from the import expect

from lang.commands.NewCommand import NewCommand


class TestNewCommand:
    def setup_method(self):

        self.lang = "/resources/lang/en/__init__.py"

    @staticmethod
    def run():

        command = NewCommand()
        return command.handle_mock()

    def test_that_lang_file_was_installed(self):

        result = self.run()
        expect(result.isfile(self.lang)).to.be.true

    def test_that_lang_file_is_not_empty(self):

        result = self.run()
        contents = result.gettext(self.lang)
        expect(contents).to.be.a(str)
        expect(contents).NOT.be.empty

    def test_that_command_works(self):

        application = Application()
        application.add(NewCommand())

        command = application.find("lang:new")
        tester = CommandTester(command)

        result = tester.execute(
            [
                ("command", command.get_name()),
                ("name", "en"),
                ("title", "English"),
                ("--mock"),
            ]
        )

        expect(result).to.be.an(int)
        expect(result).to.be(0)

        output = tester.get_display()

        expect(output).to.match("Mock mode activated")
        expect(output).to.match("Installed /resources/lang/en")
