"""
Holds the file attributes to be parsed
"""
from lang.helpers.filesystem.paths import ROOT


class File:
    kEXTENSION = "hjson"

    items = None
    filename = None
    path = None

    def __init__(self, filename, path, items=None):
        self.items = items
        self.filename = filename
        self.path = path

    def __repr__(self):
        return self.textdomain()

    def textdomain(self):

        # Remove unneeded data
        path = self.path.replace(ROOT, "")
        path = path.replace(self.filename, "")

        # Make the path standard
        path = path.lower()
        path = path.replace("/", "--")
        path = path.replace("\\", "--")
        path = path.replace(".", "-")

        # Remove the first two --
        path = path[2:]

        filename = self.filename.replace(".", "-")
        filename = filename.replace(" ", "-")
        filename = filename.lower()

        return path + filename

    def file(self):
        return self.textdomain() + "." + File.kEXTENSION
