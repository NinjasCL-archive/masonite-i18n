# coding: utf-8

from .BaseCommand import BaseCommand


class NewCommand(BaseCommand):
    """
    Creates a new language directory in /resources/lang

    lang:new
        {name : Name of the new language. Recommended ISO 639-1 code}
        {title? : Title of the new language. Defaults to name}
        {--m|mock : Mocks the filesystem for testing}
    """
    name = None
    title = None

    def get_name_and_title(self):

        if self.mock:
            name = 'en'
            title = 'English'
        else:
            name = self.argument('name')
            title = self.argument('title')

        if not title:
            title = name

        self.name = name
        self.title = title.title()

    def trigger(self):
        self.get_name_and_title()
        self.create_language(self.name, self.title)

        return self.end()
