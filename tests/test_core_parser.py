# coding: utf-8
from the import expect

from lang.core.parser import LanguageParser


class TestLanguageParser:
    def setup_method(self):
        self.opener_simple = "__("
        self.sample_text = "This text should be parsed"

    def simple_text(self, text=None):
        return "__('{}')".format(text or self.sample_text)

    def test_that_opener_simple_works(self):
        test = self.simple_text()
        result = LanguageParser.get_function_calls(test, self.opener_simple)

        expect(result).to.be.a(list)
        expect(result).to.be.NOT.empty

        translation = result[0]

        expect(translation).to.be.a(dict)
        expect(translation).to.be.NOT.empty

        expect(translation['text']).to.be.eq(self.sample_text)

