import unittest

import header
import text_formatter


class TestTextFormatter(unittest.TestCase):

    def test_empty_string(self):
        empty_string = ""
        text_header = text_formatter.make_heading(empty_string)
        result = header.is_valid_header(text_header)
        self.assertFalse(result)
    def test_new_line_string(self):
        new_line_string = "\n"
        text_header = text_formatter.make_heading(new_line_string)
        print(new_line_string)
        result = header.is_valid_header(text_header)
        self.assertFalse(result)


if __name__ == "__main__":
    TTF = TestTextFormatter()
    TTF.test_new_line_string()
    """
    TODO: implement unit tests for the function make_heading
    You need to think of the general case and edge case
    """
