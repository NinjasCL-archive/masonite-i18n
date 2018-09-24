# coding: utf-8
"""Helper functions for string parsing."""

import re


def get_text_between_string_tags(haystack: str, needle=None):

    index = 0

    if needle:
        index = haystack.find(needle, 0)

    needle = needle or ""

    begin_pos = index + len(needle)
    quotes = haystack[begin_pos]

    try:
        content = haystack[begin_pos:]
        triple = content[0] + content[1] + content[2]
        if triple == '"""' or triple == "'''":
            quotes = triple
    except IndexError:
        pass

    begin_pos = begin_pos + len(quotes)
    end_pos = haystack.find(quotes, begin_pos)

    text = haystack[begin_pos:end_pos]

    return text, begin_pos, end_pos, quotes


def get_last_parenthesis_position(haystack: str):

    stack = []
    parenthesis = {}
    open_parenthesis_count = 0
    close_parenthesis_count = 0

    for position, char in enumerate(haystack):

        if char.strip() == "":
            continue

        if char == "(":
            stack.append(position)
            open_parenthesis_count += 1

        elif char == ")":
            close_parenthesis_count += 1
            try:
                parenthesis[stack.pop()] = position
            except IndexError:
                pass

            if open_parenthesis_count == close_parenthesis_count:
                break

    final_pos = sorted(parenthesis.values(), reverse=True)[0]

    return final_pos


def get_function_params(haystack: str):

    print(haystack)

    # params = []
    # commas_stack = []
    #
    # # Find all the strings, commas should be omited if inside them
    # strings = re.findall(r'"(.*?)"', haystack)
    # strings.extend(re.findall(r"'(.*?)'", haystack))
    # strings.extend(re.findall(r"'''(.*?)'''", haystack))
    # strings.extend(re.findall(r'"""(.*?)"""', haystack))
    #
    # print(strings)
    #
    # # First search for all the positions where a comma is present
    # for position, char in enumerate(haystack):
    #
    #     if char.strip() == "":
    #         continue
    #
    #     if char == ",":
    #         content = haystack[position:]
    #         if content.find('"') ==-1:
    #             commas_stack.append(position)
    #
    # print(commas_stack)
    # for position in commas_stack:
    #     content = haystack[position:]



