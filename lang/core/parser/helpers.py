# coding: utf-8
"""Helper functions for string parsing."""
from collections import namedtuple


def starts_with_string_literal(haystack: str):
    return haystack.startswith("'") or haystack.startswith('"')


def ends_with_string_literal(haystack: str):
    return haystack.endswith("'") or haystack.endswith('"')


def starts_or_ends_with_string_literal(haystack: str):
    return starts_with_string_literal(haystack) or ends_with_string_literal(haystack)


def starts_and_ends_with_string_literal(haystack: str):
    return starts_with_string_literal(haystack) and ends_with_string_literal(haystack)


def detect_triple_quote(haystack: str, quotes=None):

    try:
        quotes = quotes or haystack[0] or None
        triple = haystack[0] + haystack[1] + haystack[2]
        if triple == '"""' or triple == "'''":
            quotes = triple
    except IndexError:
        pass

    return quotes


def get_text_between_string_tags(haystack: str, needle=None):

    index = 0
    if needle:
        index = haystack.find(needle, 0)

    needle = needle or ""

    begin_pos = index + len(needle)

    content = haystack[begin_pos:].strip()

    quotes = content[0]

    begins_with_a_string_literal = starts_with_string_literal(quotes)

    if begins_with_a_string_literal:
        quotes = detect_triple_quote(content, quotes)

    begin_pos = begin_pos + len(quotes)
    end_pos = haystack.find(quotes, begin_pos)

    if end_pos <= -1:
        raise SyntaxError("Quotes are not balanced.")

    text = haystack[begin_pos:end_pos]

    # Some times a lone " or ' char would appear in multi line strings
    # with space before the string literal
    if len(haystack[begin_pos:]) != len(content):
        if starts_with_string_literal(text):
            text = text[1:]

    if text.strip() == "":
        raise ValueError("String is Empty")

    if not begins_with_a_string_literal:
        raise ValueError("Is not a String")

    Text = namedtuple("Text", "text begin end quotes contains_string_literal")

    return Text(
        text=text,
        begin=begin_pos,
        end=end_pos,
        quotes=quotes,
        contains_string_literal=begins_with_a_string_literal,
    )


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

    if len(stack) > 0:
        raise SyntaxError("Unbalanced Parenthesis")

    final_pos = sorted(parenthesis.values(), reverse=True)[0]

    return final_pos
