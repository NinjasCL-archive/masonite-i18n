from cleo import Command


class LangCommand(Command):
    """
        Show help message for the lang namespace

        lang
    """

    def handle(self):
        self.info("Provides basic (level 1) internationalisation to Masonite.")
        self.line("")

        self.line(
            "<info>Remember to configure</info><comment> /config/language.py</comment>"
            + "<info> if you wish to change the default language.</info>"
        )

        self.line("")
        self.line(
            "<info>Type</info> <comment>craft list lang</comment>"
            + "<info>to see available commands.</info>"
        )
