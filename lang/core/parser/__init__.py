"""
Parses a file to locate all function calls containing
translatable text and their optional params.
"""

from lang.core.parser.param import Param
from lang.core.parser.item import Item
from lang.core.parser.file import File
from lang.core.parser.helpers import get_text_between_string_tags


class LanguageParser:

    kTAG_SIMPLE = "__("
    kTAG_PLURAL = "_n("

    @staticmethod
    def get_function_calls(haystack: str, needle: str):
        """
        This function will return an array of lang.core.parser.item.Item
        that holds the positions and contents of each translation function found in the haystack
        :param haystack: a string with the data
        :param needle: what needs to be found
        :return: array of lang.core.parser.item.Item
        """
        results = []

        # There is no need to continue if the string is empty
        if haystack.strip() == "":
            return results

        index = haystack.find(needle, 0)

        # Maybe regex should be used instead to match __( function calls.
        # But flexibility and readability are more important.

        while index >= 0:

            haystack = haystack[index:]

            text, begin_pos, end_pos, quotes = get_text_between_string_tags(
                haystack, needle
            )

            final_pos = haystack.find(")", end_pos)

            params = haystack[end_pos + len(quotes) : final_pos].split(",")

            items = []
            for sort, obj in enumerate(params):

                obj = obj.strip()

                if not obj == "":

                    _param = Param(sort=sort - 1, item=obj)

                    items.append(_param)

            _item = Item(
                quotes=quotes,
                begin=begin_pos,
                end=end_pos,
                text=text,
                params=items,
                needle=needle,
            )

            results.append(_item)
            index = haystack.find(needle, index + 1)

        return results

    # TODO: Implement parse function
    @staticmethod
    def parse(fs, filename):

        if not fs.exists(filename):
            raise FileNotFoundError(filename)

        path = ""
        content = fs.gettext(filename)
        items = LanguageParser.get_function_calls(content, LanguageParser.kTAG_SIMPLE)

        result = File(items, filename, path)

        return result
