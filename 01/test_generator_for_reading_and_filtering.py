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

    def test_generator_for_reading_and_filtering_case_insensitivity(self):
        file = "First line\nSecond line\nThird line"

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:

            words = ["first", "second", "third"]
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual(["First line", "Second line", "Third line"], result)

            words = ["FIRST", "THIRD"]
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual(["First line", "Third line"], result)

            expected_calls = [
                mock.call(file, 'r', encoding='utf-8'),
                mock.call(file, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file.call_args_list)

    def test_generator_for_reading_and_filtering_several_coincidence(self):
        file = "This is the first line\nThis is the second line\nThis is the third line"

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:

            words = ["the", "is"]
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual(["This is the first line", "This is the second line",
                              "This is the third line"], result)

            words = ["this", "line", "first"]
            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual(["This is the first line", "This is the second line",
                              "This is the third line"], result)

            expected_calls = [
                mock.call(file, 'r', encoding='utf-8'),
                mock.call(file, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file.call_args_list)

    def test_generator_for_reading_and_filtering_total_coincidence(self):
        file = "One\nTwo\nThree"
        words = ["One", "Two", "Three"]

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:

            result = list(generator_for_reading_and_filtering(file, words))
            self.assertEqual(["One", "Two", "Three"], result)

        mock_file.assert_called_once_with(file, 'r', encoding='utf-8')
