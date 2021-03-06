# coding: utf-8
"""Tests for the lang.core.parser package."""

from the import expect

from lang.core import parser
from lang.core.parser.file import File
from lang.core.parser.item import Item
from lang.core.parser.param import Param
from lang.helpers import open_or_make_dir
from lang.helpers.filesystem import load


class TestParser:
    def setup_method(self):
        self.tag_simple = parser.kTAG_SIMPLE
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

        result = parser.get_translation_function_calls(translation, self.tag_simple)

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
        result = parser.get_translation_function_calls(text, self.tag_simple)
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
        result = parser.get_translation_function_calls(text, self.tag_simple)

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
        result = parser.get_translation_function_calls(text, self.tag_simple)

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
        # TODO: Implement parsing params without var names like in function call 2
        text = """
                Hello this should be {{__('Parsed', comment="My Comment", note='''
                My Note''')}} successfully.
                Two function {{__("Calls", "Comment")}} with different quotes.
            """
        result = parser.get_translation_function_calls(text, self.tag_simple)

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

        # Second Function Call

        expect(item2.needle).to.eq(self.tag_simple)
        expect(item2.text).to.match("Calls")
        expect(item2.quotes).to.match('"')

        params = item2.params

        expect(params).to.be.a(list)

        # TODO: For now this will be commented. But must be validated
        # expect(len(params)).to.be.eq(1)
        #
        # params1 = params[0]
        # expect(params1).to.be.a(Param)
        # expect(params1.sort).to.be.an(int)
        # expect(params1.sort).to.be.eq(0)
        # expect(params1.sort).to.be.an(int)
        # expect(params1.item.find('"Comment"')).to.be.gt(-1)
        # expect(params1.content).to.be.a(str)
        # expect(params1.content).to.match("Comment")
        # expect(params1.type).to.match("text")

    def test_that_wrong_text_does_not_crash(self):
        text = """
                This is wrongly used {{__('Wrong'. 'Parsed' . 'Too',
                comment="My Comment", note='''
                My Note''')}}.
            """

        result = parser.get_translation_function_calls(text, self.tag_simple)

        item = result[0]
        params = item.params

        expect(len(params)).to.be.eq(2)
        expect(item.text) == "Wrong"

    def test_that_wrong_function_does_not_crash(self):
        text = """
                This is wrongly used since does not close parenthesis {{__('Wrong'}}.
            """

        result = parser.get_translation_function_calls(text, self.tag_simple)
        expect(len(result)).to.be.eq(0)

    def test_that_hash_works(self):
        text = '__("Hello")'
        sha256 = "185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969"

        result = parser.get_translation_function_calls(text, self.tag_simple)
        item = result[0]

        expect(item.hash()) == sha256

    def test_that_html_file_parser_works(self):
        # For this to work ensure that you are running tests in the
        # root directory of the project
        fs_test = load.tests()
        directory = open_or_make_dir(fs_test, "parser")
        filename = "html_file.html"
        textdomain = "tests--parser--html_file-html"

        _file = parser.parse(directory, filename)

        fs_test.close()
        directory.close()

        expect(_file).to.be.a(File)
        expect(_file.filename) == filename
        expect(_file.textdomain()) == textdomain
        expect(_file.file()) == textdomain + "." + File.kEXTENSION

        expect(_file.items).to.be.a(list)
        expect(len(_file.items)).to.be.eq(4)

        item = _file.items[1]
        expect(item).to.be.a(Item)
        expect(item.text) == "'This text also should be parsed 1"

        item = _file.items[2]
        expect(item).to.be.a(Item)
        expect(
            item.text
        ) == """'
                    This text also should be parsed 2"
                """
        expect(item.params).to.be.a(list)

        expect(len(item.params)).to.be.eq(1)

    def test_that_txt_file_parser_works(self):
        fs_test = load.tests()
        directory = open_or_make_dir(fs_test, "parser")
        filename = "txt_file.txt"
        textdomain = "tests--parser--txt_file-txt"

        _file = parser.parse(directory, filename)

        fs_test.close()
        directory.close()

        expect(_file).to.be.a(File)
        expect(_file.filename) == filename
        expect(_file.textdomain()) == textdomain
        expect(_file.file()) == textdomain + "." + File.kEXTENSION

        expect(_file.items).to.be.a(list)
        expect(len(_file.items)).to.be.eq(1)

    def test_that_python_file_parser_works(self):
        fs_test = load.tests()
        directory = open_or_make_dir(fs_test, "parser")
        filename = "python_file.py.code"
        textdomain = "tests--parser--python_file-py-code"

        _file = parser.parse(directory, filename)

        fs_test.close()
        directory.close()

        expect(_file).to.be.a(File)
        expect(_file.filename) == filename
        expect(_file.textdomain()) == textdomain
        expect(_file.file()) == textdomain + "." + File.kEXTENSION

        expect(_file.items).to.be.a(list)
        expect(len(_file.items)).to.be.eq(3)

        item = _file.items[1]
        expect(item).to.be.a(Item)
        expect(item.text) == "This {text} should be parsed too()"

        expect(len(item.params)).to.be.eq(1)

        param = item.params[0]
        print(param)
        expect(param).to.be.a(Param)
        expect(param.type).to.be.eq("comment")
        expect(param.content).to.be.eq("""( groovy      )    """)

    def test_that_emoji_file_parser_works(self):
        """test 😀_file.emoji"""
        fs_test = load.tests()
        directory = open_or_make_dir(fs_test, "parser")
        filename = "😀_file.emoji"
        textdomain = "tests--parser--😀_file-emoji"

        item = parser.parse(directory, filename)

        fs_test.close()
        directory.close()

        expect(item).to.be.a(File)
        expect(item.filename) == filename
        expect(item.textdomain()) == textdomain
        expect(item.file()) == textdomain + "." + File.kEXTENSION

        expect(item.items).to.be.a(list)
        expect(len(item.items)).to.be.eq(1)

        translation = item.items[0]
        expect(translation.text) == "😀"
