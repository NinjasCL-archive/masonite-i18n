"""
Parses a file to locate all function calls containing
translatable text and their optional comments.
"""


class LanguageParser:
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

        while index >= 0:

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
            final_pos = haystack.find(")", end_pos)

            text = haystack[begin_pos:end_pos]
            params = haystack[end_pos + len(quotes) : final_pos - len(quotes)].split(
                ","
            )

            content = []
            for sort, item in enumerate(params):
                item = item.strip()
                if not item == "":
                    content.append({"sort": sort - 1, "item": item})

            indexes.append(
                {
                    "quotes": quotes,
                    "begin": begin_pos,
                    "end": end_pos,
                    "text": text,
                    "params": content,
                    "needle": needle,
                }
            )

            index = haystack.find(needle, index + 1)

        return indexes

    def parse(self, fs, filename):

        if not fs.exists(filename):
            raise FileNotFoundError(filename)

        content = fs.gettext(filename)
        translate_simple = LanguageParser.get_function_calls(content, "__(")
        translate_plural = LanguageParser.get_function_calls(content, "_n(")
