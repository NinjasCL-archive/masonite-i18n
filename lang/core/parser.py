"""
Parses a file to locate all function calls containing
translatable text and their optional params.
"""


class LanguageParser:

    kTAG_SIMPLE = "__("
    kTAG_PLURAL = "_n("

    @staticmethod
    def get_text_between_string_tags(haystack, needle=None):

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

    @staticmethod
    def get_function_calls(haystack, needle):
        """
        This function will return an array of dictionaries
        that holds the positions and contents of each translation function found in the haystack
        :param haystack: a string with the data
        :param needle: what needs to be found
        :return: array of dict
        """
        indexes = []
        index = haystack.find(needle, 0)

        # Maybe regex should be used instead to match __( function calls.
        # But flexibility and readability are more important.

        while index >= 0:

            haystack = haystack[index:]

            text, begin_pos, end_pos, quotes = LanguageParser.get_text_between_string_tags(
                haystack, needle
            )

            final_pos = haystack.find(")", end_pos)

            params = haystack[end_pos + len(quotes) : final_pos].split(",")

            items = []
            for sort, item in enumerate(params):
                item = item.strip()

                if not item == "":

                    item_type = "text"
                    should_split = True

                    if item.find("comment") > -1:
                        item_type = "comment"
                    elif item.find("note") > -1:
                        item_type = "note"
                    elif item.find("textdomain") > -1:
                        item_type = "textdomain"
                    else:
                        should_split = False

                    item_content = item

                    if should_split:
                        parts = item.split("=")
                        item_content = parts[1]

                    item_content = LanguageParser.get_text_between_string_tags(
                        item_content
                    )[0]

                    items.append(
                        {
                            "sort": sort - 1,
                            "item": item,
                            "type": item_type,
                            "content": item_content,
                        }
                    )

            indexes.append(
                {
                    "quotes": quotes,
                    "begin": begin_pos,
                    "end": end_pos,
                    "text": text,
                    "params": items,
                    "needle": needle,
                }
            )

            index = haystack.find(needle, index + 1)

        return indexes

    def parse(self, fs, filename):

        if not fs.exists(filename):
            raise FileNotFoundError(filename)

        content = fs.gettext(filename)
        get_simple = LanguageParser.get_function_calls(
            content, LanguageParser.kTAG_SIMPLE
        )
        translate_plural = LanguageParser.get_function_calls(
            content, LanguageParser.kTAG_PLURAL
        )
