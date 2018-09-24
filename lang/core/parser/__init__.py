# coding: utf-8
"""
Provides parsing functions to text.

Parses a file to locate all function calls containing.
translatable text function calls and their optional params.
"""

from lang.core.parser.param import Param
from lang.core.parser.item import Item
from lang.core.parser.file import File
from lang.core.parser.helpers import get_text_between_string_tags, \
    get_last_parenthesis_position, get_trailing_components


kTAG_SIMPLE = "__("
kTAG_PLURAL = "_n("


def get_translation_function_calls(haystack: str, needle: str):
    """
    Return an array of lang.core.parser.item.Item.

    Obtain the positions and contents of each translation function found in the haystack.

    :param haystack: a string with the data.
    :param needle: what needs to be found.
    :return: array of lang.core.parser.item.Item.
    """
    results = []

    # There is no need to continue if the string is empty
    if haystack.strip() == "":
        return results

    index = haystack.find(needle, 0)

    # Maybe regex should be used instead to match __( function calls.
    # But flexibility and readability are more important.

    while index >= 0:

        # First we need the translatable string
        content = haystack[index:]

        text, begin_pos, end_pos, quotes, begins_with_a_string_literal = get_text_between_string_tags(
            content, needle
        )

        if not begins_with_a_string_literal:
            index = haystack.find(needle, index + 1)
            continue

        init_pos = end_pos + len(quotes)
        final_pos = get_last_parenthesis_position(content)
        params = content[init_pos : final_pos]

        get_trailing_components(params)

        params = params.split(",")

        # Parse the param contents to simplify handling later
        items = []

        for sort, obj in enumerate(params):
                obj = obj.strip()
                if obj == "":
                    continue
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


def parse(fs, filename: str):
    """
    Obtain the contents of a file and search for translatable strings.

    :param fs: pyfilesystem instance.
    :param filename: string with the filename to extract the translatable strings.
    :return: lang.core.parser.file.File instance.
    """
    if not fs.exists(filename):
        raise FileNotFoundError(filename)

    path = fs.desc(filename)

    content = fs.gettext(filename)

    # TODO: Implement more tags in the future
    items = get_translation_function_calls(content, kTAG_SIMPLE)

    result = File(filename, path, items)

    return result
