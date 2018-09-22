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
