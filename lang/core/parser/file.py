"""
Holds the file attributes to be parsed
"""


class File:

    items = None
    filename = None
    path = None
    extension = "hjson"

    def __init__(self, items=None, filename=None, path=None):
        self.items = items
        self.filename = filename
        self.path = path

    def __repr__(self):
        return self.textdomain()

    def textdomain(self):
        path = self.path.replace("/", "--")
        path = path.replace("\\", "--")
        path = path.lower()

        filename = self.filename.replace(".", "-")
        filename = filename.replace(" ", "-")
        filename = filename.lower()

        return path + filename

    def file(self):
        return self.textdomain() + "." + self.extension
