import unittest
from unittest import mock
import io

from generator_for_reading_and_filtering import generator_for_reading_and_filtering


class TestGeneratorForReadingAndFiltering(unittest.TestCase):

    def test_generator_for_reading_and_filtering_total(self):
        file = "First line\nSecond line\nThird line"
        words = ["First", "Second", "Third"]

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual(["First line", "Second line", "Third line"], result)

        mock_file.assert_called_once_with(file, 'r', encoding='utf-8')

    def test_generator_for_reading_and_filtering_partial(self):
        file = "First line\nSecond line\nThird line"
        words = ["First", "Third"]

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual(["First line", "Third line"], result)

        mock_file.assert_called_once_with(file, 'r', encoding='utf-8')

    def test_generator_for_reading_and_filtering_empty(self):
        file = "First line\nSecond line\nThird line"
        words = ["One", "Two", "Three"]

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual([], result)

        mock_file.assert_called_once_with(file, 'r', encoding='utf-8')

    def test_generator_for_reading_and_filtering_file_object(self):
        file = io.StringIO("First line\nSecond line\nThird line")
        words = ["First", "Second", "Third"]

        result = list(generator_for_reading_and_filtering(file, words))
        self.assertEqual(["First line", "Second line", "Third line"], result)
        file.close()

    def test_generator_for_reading_and_filtering_empty_file(self):
        file = ""
        words = ["First", "Second", "Third"]

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual([], result)

        mock_file.assert_called_once_with(file, 'r', encoding='utf-8')

    def test_generator_for_reading_and_filtering_empty_words(self):
        file = "First line\nSecond line\nThird line"
        words = []

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual([], result)

        mock_file.assert_called_once_with(file, 'r', encoding='utf-8')

    def test_generator_for_reading_and_filtering_without_words(self):
        file = "First line\nSecond line\nThird line"

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            result = list(generator_for_reading_and_filtering(file))
            self.assertEqual([], result)

        mock_file.assert_called_once_with(file, 'r', encoding='utf-8')

    def test_generator_for_reading_and_filtering_without_file(self):
        with self.assertRaises(TypeError) as err:
            list(generator_for_reading_and_filtering())

        self.assertEqual("input filename or file object", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))
