# coding: utf-8
from the import expect
from lang.helpers.filesystem import load
from lang.helpers import open_or_make_dir
from lang import package_directory
from lang.core.parser import LanguageParser
from lang.core.parser.file import File
from lang.core.parser.item import Item
from lang.core.parser.param import Param


class TestLanguageParser:
    def setup_method(self):
        self.tag_simple = LanguageParser.kTAG_SIMPLE
        self.sample_text = "This text should be parsed"

    def simple_text_single_quote(self, text=None):
        text = text or self.sample_text
        return "__('{}')".format(text)

    def simple_text_double_quote(self, text=None):
        text = text or self.sample_text
        return '__("{}")'.format(text)

    def simple_text_triple_single_quote(self, text=None):
        text = text or self.sample_text
        return "__('''{}''')".format(text)

    def simple_text_triple_double_quote(self, text=None):
        text = text or self.sample_text
        return '__("""{}""")'.format(text)

    def simple_text_test(self, translation, text):

        result = LanguageParser.get_function_calls(translation, self.tag_simple)

        expect(result).to.be.a(list)
        expect(result).to.be.NOT.empty

        expect(len(result)).to.be.eq(1)

        item = result[0]

        expect(item).to.be.a(Item)
        expect(item).to.be.NOT.empty

        assert item.needle == self.tag_simple

        # expect(item.text).to.match(text) have problems with parenthesis inside text
        assert item.text == text

        return item

    def test_that_empty_returns_zero_items(self):
        text = ""
        result = LanguageParser.get_function_calls(text, self.tag_simple)
        expect(result).to.be.a(list)
        expect(len(result)).to.be.eq(0)

    def test_that_single_char_text_works(self):
        text = "H"
        item = self.simple_text_test(self.simple_text_single_quote(text), text)
        expect(item.quotes).to.match("'")

    def test_that_weird_char_text_works(self):
        text = '()()(sd)()"""'
        item = self.simple_text_test(self.simple_text_single_quote(text), text)
        expect(item.quotes).to.match("'")

    def test_that_simple_text_works(self):
        item = self.simple_text_test(self.simple_text_single_quote(), self.sample_text)
        expect(item.quotes).to.match("'")

    def test_that_simple_text_double_quote_works(self):
        item = self.simple_text_test(self.simple_text_double_quote(), self.sample_text)
        expect(item.quotes).to.match('"')

    def test_that_simple_text_triple_single_quote_works(self):
        item = self.simple_text_test(
            self.simple_text_triple_single_quote(), self.sample_text
        )
        expect(item.quotes).to.match("'''")

    def test_that_simple_text_triple_double_quote_works(self):
        item = self.simple_text_test(
            self.simple_text_triple_double_quote(), self.sample_text
        )
        expect(item.quotes).to.match('"""')

    def test_that_complex_text_works(self):
        text = """
            Hello this should be __('Parsed') successfully.
            Two function __("Calls") with different quotes.
        """
        result = LanguageParser.get_function_calls(text, self.tag_simple)

        expect(result).to.be.a(list)
        expect(result).to.be.NOT.empty

        expect(len(result)).to.be.eq(2)

        item = result[0]
        item2 = result[1]

        expect(item).to.be.a(Item)
        expect(item).to.be.NOT.empty

        expect(item.needle).to.eq(self.tag_simple)
        expect(item.text).to.match("Parsed")
        expect(item.quotes).to.match("'")

        expect(item2).to.be.a(Item)
        expect(item2).to.be.NOT.empty

        expect(item2.needle).to.eq(self.tag_simple)
        expect(item2.text).to.match("Calls")
        expect(item2.quotes).to.match('"')

    def test_that_jinja_text_works(self):
        text = """
                Hello this should be {{__('Parsed')}} successfully.
                Two function {{__("Calls")}} with different quotes.
            """
        result = LanguageParser.get_function_calls(text, self.tag_simple)

        expect(result).to.be.a(list)
        expect(result).to.be.NOT.empty

        expect(len(result)).to.be.eq(2)

        item = result[0]
        item2 = result[1]

        expect(item).to.be.a(Item)
        expect(item).to.be.NOT.empty

        expect(item.needle).to.eq(self.tag_simple)
        expect(item.text).to.match("Parsed")
        expect(item.quotes).to.match("'")

        expect(item2).to.be.a(Item)
        expect(item2).to.be.NOT.empty

        expect(item2.needle).to.eq(self.tag_simple)
        expect(item2.text).to.match("Calls")
        expect(item2.quotes).to.match('"')

    def test_that_text_with_params_works(self):
        text = """
                Hello this should be {{__('Parsed', comment="My Comment", note='''
                My Note''')}} successfully.
                Two function {{__("Calls", "Comment")}} with different quotes.
            """
        result = LanguageParser.get_function_calls(text, self.tag_simple)

        expect(result).to.be.a(list)
        expect(result).to.be.NOT.empty

        expect(len(result)).to.be.eq(2)

        item = result[0]
        item2 = result[1]

        expect(item).to.be.a(Item)
        expect(item).to.be.NOT.empty

        expect(item.needle).to.eq(self.tag_simple)
        expect(item.text).to.match("Parsed")
        expect(item.quotes).to.match("'")

        params = item.params

        expect(params).to.be.a(list)
        expect(len(params)).to.be.eq(2)

        params1 = params[0]
        expect(params1).to.be.a(Param)
        expect(params1.sort).to.be.an(int)
        expect(params1.sort).to.be.eq(0)
        expect(params1.item).to.be.a(str)
        expect(params1.item.find('comment="My Comment"')).to.be.gt(-1)
        expect(params1.content).to.be.a(str)
        expect(params1.content).to.match("My Comment")
        expect(params1.type).to.match("comment")

        params2 = params[1]
        expect(params2.sort).to.be.an(int)
        expect(params2.sort).to.be.eq(1)
        expect(params2.item).to.be.a(str)

        expect(
            params2.item.find(
                """note='''
                My Note'''"""
            )
        ).to.be.gt(-1)

        expect(params2.content).to.be.a(str)
        expect(params2.content).to.match(
            """
                My Note"""
        )
        expect(params2.type).to.match("note")

        expect(item2).to.be.a(Item)
        expect(item2).to.be.NOT.empty

        expect(item2.needle).to.eq(self.tag_simple)
        expect(item2.text).to.match("Calls")
        expect(item2.quotes).to.match('"')

        params = item2.params

        expect(params).to.be.a(list)
        expect(len(params)).to.be.eq(1)

        params1 = params[0]
        expect(params1).to.be.a(Param)
        expect(params1.sort).to.be.an(int)
        expect(params1.sort).to.be.eq(0)
        expect(params1.sort).to.be.an(int)
        expect(params1.item.find('"Comment"')).to.be.gt(-1)
        expect(params1.content).to.be.a(str)
        expect(params1.content).to.match("Comment")
        expect(params1.type).to.match("text")

    def test_that_wrong_text_does_not_crash(self):
        text = """
                This is wrongly used {{__('Wrong'. 'Parsed' . 'Too', comment="My Comment", note='''
                My Note''')}}.
            """

        result = LanguageParser.get_function_calls(text, self.tag_simple)

        item = result[0]
        params = item.params

        expect(len(params)).to.be.eq(3)
        expect(item.text) == "Wrong"

    def test_that_hash_works(self):
        text = '__("Hello")'
        sha256 = "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"

        result = LanguageParser.get_function_calls(text, self.tag_simple)
        item = result[0]

        expect(item.hash()) == sha256

    def test_that_html_file_parser_works(self):
        # For this to work ensure that you are running tests in the root directory of the project
        fs_test = load.tests()
        directory = open_or_make_dir(fs_test, "parser")
        filename = "html_file.html"
        textdomain = "tests--parser--html_file-html"

        item = LanguageParser.parse(directory, filename)

        fs_test.close()
        directory.close()

        expect(item).to.be.a(File)
        expect(item.filename) == filename
        expect(item.textdomain()) == textdomain
        expect(item.file()) == textdomain + "." + File.kEXTENSION

        expect(item.items).to.be.a(list)
        expect(len(item.items)).to.be.eq(2)

    def test_that_txt_file_parser_works(self):
        fs_test = load.tests()
        directory = open_or_make_dir(fs_test, "parser")
        filename = "txt_file.txt"
        textdomain = "tests--parser--txt_file-txt"

        item = LanguageParser.parse(directory, filename)

        fs_test.close()
        directory.close()

        expect(item).to.be.a(File)
        expect(item.filename) == filename
        expect(item.textdomain()) == textdomain
        expect(item.file()) == textdomain + "." + File.kEXTENSION

        expect(item.items).to.be.a(list)
        expect(len(item.items)).to.be.eq(1)

    def test_that_python_file_parser_works(self):
        fs_test = load.tests()
        directory = open_or_make_dir(fs_test, "parser")
        filename = "python_file.py.code"
        textdomain = "tests--parser--python_file-py-code"

        item = LanguageParser.parse(directory, filename)

        fs_test.close()
        directory.close()

        expect(item).to.be.a(File)
        expect(item.filename) == filename
        expect(item.textdomain()) == textdomain
        expect(item.file()) == textdomain + "." + File.kEXTENSION

        expect(item.items).to.be.a(list)
        expect(len(item.items)).to.be.eq(1)




