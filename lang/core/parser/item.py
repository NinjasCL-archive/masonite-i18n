"""
Holds the item for each translation function found in the file
"""
import hashlib


class Item:
    quotes = None
    begin = None
    end = None
    text = None
    params = None
    needle = None

    def __init__(
        self, quotes=None, begin=None, end=None, text=None, params=None, needle=None
    ):
        self.quotes = quotes
        self.begin = begin
        self.end = end
        self.text = text
        self.params = params
        self.needle = needle

    def __repr__(self):
        return self.text

    def hash(self):
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()
