import unittest
from unittest import mock
from parse_json import parse_json


class TestParseJson(unittest.TestCase):
    def setUp(self):
        self.jsn = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        self.mock_keyword_callback = mock.Mock("parse_json.keyword_callback_function",
                                               return_value=None)

    def test_parse_json_simple(self):

        required_fields = ["key1"]
        keywords = ["word2"]

        self.assertEqual(None, parse_json(self.jsn, required_fields, keywords,
                                          keyword_callback=self.mock_keyword_callback))

        expected_calls = [
            mock.call("word2"),
        ]
        self.assertEqual(expected_calls, self.mock_keyword_callback.mock_calls)

    def test_parse_json_without_required_fields(self):
        keywords = ["word2"]

        with self.assertRaises(TypeError) as err:
            self.assertEqual(None, parse_json(self.jsn, keywords=keywords,
                                              keyword_callback=self.mock_keyword_callback))

        self.assertEqual("required_fields and keywords should be a list of str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        self.assertEqual([], self.mock_keyword_callback.mock_calls)

    def test_parse_json_without_keywords(self):
        required_fields = ["key1"]

        with self.assertRaises(TypeError) as err:
            self.assertEqual(None, parse_json(self.jsn, required_fields,
                                              keyword_callback=self.mock_keyword_callback))

        self.assertEqual("required_fields and keywords should be a list of str", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))

        self.assertEqual([], self.mock_keyword_callback.mock_calls)

    def test_parse_json_with_several_fields(self):
        required_fields = ["key1", "key2"]
        keywords = ["word2"]

        self.assertEqual(None, parse_json(self.jsn, required_fields, keywords,
                                          keyword_callback=self.mock_keyword_callback))

        expected_calls = [
            mock.call("word2"),
            mock.call("word2"),
        ]
        self.assertEqual(expected_calls, self.mock_keyword_callback.mock_calls)

    def test_parse_json_no_found_keywords(self):
        required_fields = ["key1"]
        keywords = ["word3"]

        self.assertEqual(None, parse_json(self.jsn, required_fields, keywords,
                                          keyword_callback=self.mock_keyword_callback))

        self.assertEqual([], self.mock_keyword_callback.mock_calls)

    def test_parse_json_no_found_required_field(self):
        required_fields = ["key3"]
        keywords = ["word3"]

        self.assertEqual(None, parse_json(self.jsn, required_fields, keywords,
                                          keyword_callback=self.mock_keyword_callback))

        self.assertEqual([], self.mock_keyword_callback.mock_calls)

    def test_parse_json_partial_keyword(self):
        required_fields = ["key1"]
        keywords = ["word"]

        self.assertEqual(None, parse_json(self.jsn, required_fields, keywords,
                                          keyword_callback=self.mock_keyword_callback))

        self.assertEqual([], self.mock_keyword_callback.mock_calls)
