# coding: utf-8
"""Holds the params after the string to translate."""
import tokenize
from io import BytesIO

from .helpers import get_text_between_string_tags

COMMENT = "comment"
NOTE = "note"
TEXTDOMAIN = "textdomain"


class Param:
    sort = None
    item = None
    type = None
    content = None

    def __init__(self, category: str, content: str, sort: int, raw: str = None):
        self.sort = sort
        self.type = category
        self.content = content
        self.item = raw

    @staticmethod
    def __tokenize(haystack: str):
        wrapper = BytesIO(haystack.encode("utf-8"))
        return tokenize.tokenize(wrapper.readline)

    @staticmethod
    def __get_tokens(haystack: str):

        # Convert to a valid python function
        string = "t(%s)" % haystack

        try:
            tokens = Param.__tokenize(string)
        except tokenize.TokenError:
            pass

        return tokens

    @staticmethod
    def get_params(haystack: str):

        if haystack.startswith(",") or haystack.startswith("."):
            haystack = haystack[1:]

        haystack = haystack.strip()

        tokens = Param.__get_tokens(haystack)
        is_valid_category = False
        category = None

        params = []

        sort = 0
        for index, token in enumerate(tokens):

            string = token.string.lower().strip()
            if string == "":
                continue

            if token.type == tokenize.NAME:

                if string == COMMENT or string == NOTE or string == TEXTDOMAIN:
                    is_valid_category = True
                    category = string
                    continue

            if token.type == tokenize.STRING:

                if is_valid_category:
                    content = get_text_between_string_tags(token.string).text
                    if not content.strip() == "":
                        params.append(Param(category, content, sort, token.line))
                        sort += 1

                    # Reset for the next token
                    is_valid_category = False
                    category = None
                    continue

        return params

    def __repr__(self):
        return self.content
