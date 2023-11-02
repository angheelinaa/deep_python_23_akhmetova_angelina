import unittest
import threading
import io
from unittest import mock
from contextlib import redirect_stdout
from server import run_server, fetch_url, COUNT_URLS
from client import run_client


class TestClientServerApp(unittest.TestCase):
    def test_fetch_url(self):
        url = "https://ru.wikipedia.org/wiki/Python"
        k = 5
        expected_value = {'python': 445, 'в': 323, 'и': 293, 'с': 162, 'на': 148}
        self.assertEqual(expected_value, fetch_url(url, k))
        self.assertEqual(k, len(fetch_url(url, k)))

    def test_fetch_url_error(self):
        url = "https://ru.wikipedia.org/wiki/Pythonist"
        k = 5
        with redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(None, fetch_url(url, k))

        self.assertEqual(f"url '{url}' not found", stdout.getvalue().strip())

    @mock.patch('server.fetch_url')
    def test_client_server_simple(self, mock_fetch_url):
        mock_fetch_url.return_value = {'python': 445, 'в': 323, 'и': 293, 'с': 162, 'на': 148}
        file = "https://ru.wikipedia.org/wiki/Python"
        k = 5

        server_thread = threading.Thread(target=run_server, args=(10, k), name='server_thread')
        server_thread.start()
        self.assertEqual(2, threading.active_count())

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            self.assertEqual(None, run_client(10, file))
            active_workers = [i for i in threading.enumerate()
                              if i.name.startswith("ThreadPoolExecutor")]
            self.assertLessEqual(len(active_workers), 10)

            expected_calls = [
                mock.call(file, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file.call_args_list)

        self.assertEqual(1, COUNT_URLS[0])
        server_thread.join()
        self.assertEqual(1, threading.active_count())
        self.assertEqual([mock.call(file, k)], mock_fetch_url.mock_calls)

    @mock.patch('server.fetch_url')
    def test_client_server_url_not_found(self, mock_fetch_url):
        mock_fetch_url.return_value = None
        file = "https://ru.wikipedia.org/wiki/Pythonist"
        k = 5

        server_thread = threading.Thread(target=run_server, args=(10, k), name='server_thread')
        server_thread.start()
        self.assertEqual(2, threading.active_count())

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            self.assertEqual(None, run_client(10, file))
            active_workers = [i for i in threading.enumerate()
                              if i.name.startswith("ThreadPoolExecutor")]
            self.assertLessEqual(len(active_workers), 10)

            expected_calls = [
                mock.call(file, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file.call_args_list)

        self.assertEqual(0, COUNT_URLS[0])
        server_thread.join()
        self.assertEqual(1, threading.active_count())
        self.assertEqual([mock.call(file, k)], mock_fetch_url.mock_calls)

    @mock.patch('server.fetch_url')
    def test_server_timeout(self, mock_fetch_url):
        server_thread = threading.Thread(target=run_server, args=(10, 7), name='server_thread')
        server_thread.start()
        self.assertEqual(2, threading.active_count())

        self.assertEqual(0, COUNT_URLS[0])
        server_thread.join()
        self.assertEqual(1, threading.active_count())
        self.assertEqual([], mock_fetch_url.mock_calls)

    @mock.patch('server.fetch_url')
    def test_client_server_several_urls(self, mock_fetch_url):
        file = "https://habr.com/ru/articles/771116/" + '\n' \
               "https://habr.com/ru/articles/771052/" + '\n' \
               "https://habr.com/ru/articles/771050/"
        k = 5
        expected_values = [
            {"в": 11, "windows": 10, "microsoft": 8, "mvp": 7, "insider": 6},
            {"в": 20, "threads": 19, "и": 15, "meta": 15, "software": 7},
            {"с": 13, "на": 8, "macbook": 7, "touch": 7, "bar": 7},
        ]
        mock_fetch_url.side_effect = [expected_values[0], expected_values[1], expected_values[2]]

        server_thread = threading.Thread(target=run_server, args=(10, k), name='server_thread')
        server_thread.start()
        self.assertEqual(2, threading.active_count())

        with mock.patch('builtins.open', mock.mock_open(read_data=file)) as mock_file:
            self.assertEqual(None, run_client(10, file))
            active_workers = [i for i in threading.enumerate()
                              if i.name.startswith("ThreadPoolExecutor")]
            self.assertLessEqual(len(active_workers), 10)

            expected_calls = [
                mock.call(file, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file.call_args_list)

        self.assertEqual(3, COUNT_URLS[0])
        server_thread.join()
        self.assertEqual(1, threading.active_count())
        expected_calls = [
            mock.call("https://habr.com/ru/articles/771116/", k),
            mock.call("https://habr.com/ru/articles/771052/", k),
            mock.call("https://habr.com/ru/articles/771050/", k),
        ]
        self.assertEqual(expected_calls, mock_fetch_url.mock_calls)

    @mock.patch('server.fetch_url')
    def test_client_server_several_clients(self, mock_fetch_url):
        file_1 = "https://habr.com/ru/articles/771116/"
        file_2 = "https://habr.com/ru/articles/771052/"
        file_3 = "https://habr.com/ru/articles/771050/"
        k = 5
        expected_values = [
            {"в": 11, "windows": 10, "microsoft": 8, "mvp": 7, "insider": 6},
            {"в": 20, "threads": 19, "и": 15, "meta": 15, "software": 7},
            {"с": 13, "на": 8, "macbook": 7, "touch": 7, "bar": 7},
        ]
        mock_fetch_url.side_effect = [expected_values[0], expected_values[1], expected_values[2]]

        server_thread = threading.Thread(target=run_server, args=(10, k), name='server_thread')
        server_thread.start()
        self.assertEqual(2, threading.active_count())

        with mock.patch('builtins.open', mock.mock_open(read_data=file_1)) as mock_file_1:
            self.assertEqual(None, run_client(10, file_1))
            active_workers = [i for i in threading.enumerate()
                              if i.name.startswith("ThreadPoolExecutor")]
            self.assertLessEqual(len(active_workers), 10)

            expected_calls = [
                mock.call(file_1, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file_1.call_args_list)

        self.assertEqual(1, COUNT_URLS[0])
        expected_calls = [
            mock.call("https://habr.com/ru/articles/771116/", k),
        ]
        self.assertEqual(expected_calls, mock_fetch_url.mock_calls)

        with mock.patch('builtins.open', mock.mock_open(read_data=file_2)) as mock_file_2:
            self.assertEqual(None, run_client(10, file_2))
            active_workers = [i for i in threading.enumerate()
                              if i.name.startswith("ThreadPoolExecutor")]
            self.assertLessEqual(len(active_workers), 10)

            expected_calls = [
                mock.call(file_2, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file_2.call_args_list)

        self.assertEqual(2, COUNT_URLS[0])
        expected_calls = [
            mock.call("https://habr.com/ru/articles/771116/", k),
            mock.call("https://habr.com/ru/articles/771052/", k),
        ]
        self.assertEqual(expected_calls, mock_fetch_url.mock_calls)

        with mock.patch('builtins.open', mock.mock_open(read_data=file_3)) as mock_file_3:
            self.assertEqual(None, run_client(10, file_3))
            active_workers = [i for i in threading.enumerate()
                              if i.name.startswith("ThreadPoolExecutor")]
            self.assertLessEqual(len(active_workers), 10)

            expected_calls = [
                mock.call(file_3, 'r', encoding='utf-8'),
            ]
            self.assertEqual(expected_calls, mock_file_3.call_args_list)

        self.assertEqual(3, COUNT_URLS[0])
        server_thread.join()
        self.assertEqual(1, threading.active_count())
        expected_calls = [
            mock.call("https://habr.com/ru/articles/771116/", k),
            mock.call("https://habr.com/ru/articles/771052/", k),
            mock.call("https://habr.com/ru/articles/771050/", k),
        ]
        self.assertEqual(expected_calls, mock_fetch_url.mock_calls)
