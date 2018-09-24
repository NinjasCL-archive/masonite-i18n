# coding: utf-8
"""Helper functions for string parsing."""


def get_text_between_string_tags(haystack: str, needle=None):

    index = 0
    if needle:
        index = haystack.find(needle, 0)

    needle = needle or ""

    begin_pos = index + len(needle)

    content = haystack[begin_pos:].strip()

    quotes = content[0]

    begins_with_a_string_literal = (quotes.startswith('"') or quotes.startswith("'"))

    if begins_with_a_string_literal:
        try:
            triple = content[0] + content[1] + content[2]
            if triple == '"""' or triple == "'''":
                quotes = triple
        except IndexError:
            pass

    begin_pos = begin_pos + len(quotes)
    end_pos = haystack.find(quotes, begin_pos)

    text = haystack[begin_pos:end_pos]

    # Some times a lone " or ' char would appear in multiline strings
    if text.startswith('"') or text.startswith("'"):
        text = text[1:]

    return text, begin_pos, end_pos, quotes, begins_with_a_string_literal


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



