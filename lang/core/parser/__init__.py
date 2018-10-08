# coding: utf-8
"""
Provides parsing functions to text.

Parses a file to locate all function calls containing.
translatable text function calls and their optional params.
"""

from lang.core.parser.param import Param
from lang.core.parser.item import Item
from lang.core.parser.file import File
from lang.core.parser.helpers import (
    get_text_between_string_tags,
    get_last_parenthesis_position,
)

kTAG_SIMPLE = "__("
kTAG_PLURAL = "_n("


def step(haystack: str, needle: str, index: int):
    return haystack.find(needle, index + 1)


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

        try:
            result = get_text_between_string_tags(content, needle)
            # Only parse functions with balanced parenthesis
            final_pos = get_last_parenthesis_position(content)

        except (SyntaxError, ValueError, IndexError):
            # Unbalanced quotes, parenthesis or wrong syntax found
            index = step(haystack, needle, index)
            continue

        init_pos = result.end + len(result.quotes)
        params = content[init_pos:final_pos].strip()

        if len(params) > 0:
            params = Param.get_params(params)

        _item = Item(
            quotes=result.quotes,
            begin=result.begin,
            end=result.end,
            text=result.text,
            params=params,
            needle=needle,
        )

        results.append(_item)

        index = step(haystack, needle, index)

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

    result = File(filename, path, items, content)

    return result
