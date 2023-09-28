import unittest
from unittest import mock
import time
import io
from contextlib import redirect_stdout
from decorator_mean import mean


class TestMean(unittest.TestCase):
    def test_mean_correct_decorator(self):
        mock_func = mock.Mock(return_value="result")
        decorated_func = mean(1)(mock_func)

        self.assertEqual("result", decorated_func())

        expected_calls = [mock.call()]
        self.assertEqual(expected_calls, mock_func.mock_calls)

    def test_mean_simple(self):
        @mean(1)
        def func():
            time.sleep(1)
            return "result"

        with redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual("result", func())

        self.assertLess(abs(float(stdout.getvalue().strip()) - 1), 0.002)

    def test_mean_several_calls(self):
        @mean(2)
        def func():
            time.sleep(0.5)
            return "result"

        with redirect_stdout(io.StringIO()) as stdout:
            for _ in range(10):
                self.assertEqual("result", func())

        for value in stdout.getvalue().strip().split():
            self.assertLess(abs(float(value) - 0.5), 0.002)

    def test_mean_count_calls_less_k(self):
        @mean(3)
        def func():
            time.sleep(1)
            return "result"

        with redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual("result", func())
            self.assertEqual("result", func())

        value_1, value_2 = stdout.getvalue().strip().split()
        self.assertLess(abs(float(value_1) - 1), 0.002)
        self.assertLess(abs(float(value_2) - 1), 0.002)
