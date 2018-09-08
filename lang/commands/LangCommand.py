from cleo import Command


class LangCommand(Command):
    """
        Show help message for the lang namespace

        lang
    """
    def handle(self):
        self.info('Provides basic (level 1) internationalisation to Masonite.')
        self.info('')
        self.info('Remember to configure /config/language.py if you wish to change the default language.')
        self.info('Be sure to configure /config/middleware.py too and add the middleware for language detection.')
        self.info('')
        self.info('Type craft list lang to see available commands.')
