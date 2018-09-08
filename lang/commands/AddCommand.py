# coding: utf-8

from .BaseCommand import BaseCommand


class AddCommand(BaseCommand):
    """
    Adds a translation file to the desired translation directory

    lang:add
        {file : path to the file to add a translation}
        {lang? : language directory for use. if not given uses the default directory}
    """

    def trigger(self):
        pass
