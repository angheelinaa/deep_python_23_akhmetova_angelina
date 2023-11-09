import unittest
import json
import io
import asyncio
from contextlib import redirect_stdout
from unittest import mock
from fetcher import batch_fetch, fetch_url, url_parser


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    async def test_url_parser(self):
        url = "https://example.com"
        expected_value = "<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'>" \
                         "<title>Простая страница </title></head>" \
                         "<body>Контент этой страницы </body></html>"
        common_words = {'простая': 1, 'страница': 1, 'контент': 1, 'этой': 1}
        mock_resp = mock.AsyncMock()
        mock_resp.text.return_value = expected_value

        with redirect_stdout(io.StringIO()) as stdout:
            await url_parser(url, mock_resp)

        self.assertEqual(f"{url}: {json.dumps(common_words, ensure_ascii=False)}",
                         stdout.getvalue().strip())
        mock_resp.assert_not_awaited()
        mock_resp.text.assert_awaited_once()

    async def test_fetch_url(self):
        url = "https://example.com"
        expected_value = "<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'>" \
                         "<title>Простая страница </title></head>" \
                         "<body>Контент этой страницы </body></html>"
        common_words = {'простая': 1, 'страница': 1, 'контент': 1, 'этой': 1}
        sem = asyncio.Semaphore(10)

        mock_resp = mock.AsyncMock()
        mock_resp.status = 200
        mock_resp.text.return_value = expected_value

        with mock.patch('fetcher.aiohttp.ClientSession.get') as mock_session:
            mock_session.return_value.__aenter__.return_value = mock_resp
            with redirect_stdout(io.StringIO()) as stdout:
                await fetch_url(url, sem)

        self.assertEqual(f"{url}: {json.dumps(common_words, ensure_ascii=False)}",
                         stdout.getvalue().strip())
        mock_resp.assert_not_awaited()
        mock_resp.text.assert_awaited_once()
        mock_session.assert_called_once_with(url)

    @mock.patch('fetcher.aiohttp.ClientSession.get')
    async def test_fetch_url_not_found(self, mock_session):
        url = "https://example.com"
        sem = asyncio.Semaphore(10)

        mock_resp = mock.AsyncMock()
        mock_resp.status = 404
        mock_session.return_value.__aenter__.return_value = mock_resp

        with redirect_stdout(io.StringIO()) as stdout:
            with self.assertRaises(Exception):
                await fetch_url(url, sem)

        self.assertEqual(f"url '{url}' not found", stdout.getvalue().strip())
        mock_resp.assert_not_awaited()
        mock_session.assert_called_once_with(url)

    @mock.patch('fetcher.aiohttp.ClientSession.get')
    async def test_batch_fetch(self, mock_session):
        filename = './url.txt'
        expected_value = []
        common_words = []
        with open(filename, 'w', encoding='UTF-8') as file:
            for i in range(3):
                file.write(f"https://example.com/{i}\n")
                expected_value.append(
                    f"<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'>"
                    f"<title>Простая {i} страница </title></head>"
                    f"<body>Контент этой {i} страницы </body></html>"
                )
                common_words.append({f'{i}': 2, 'простая': 1, 'страница': 1, 'контент': 1})

        mock_resp = mock.AsyncMock()
        mock_resp.status = 200
        mock_resp.text.side_effect = expected_value
        mock_session.return_value.__aenter__.return_value = mock_resp

        with redirect_stdout(io.StringIO()) as stdout:
            await batch_fetch(10, filename)

        for i in range(3):
            url = f"https://example.com/{i}"
            self.assertEqual(f"{url}: {json.dumps(common_words[i], ensure_ascii=False)}",
                             stdout.getvalue().strip().split('\n')[i])

        mock_resp.assert_not_awaited()
        self.assertEqual(3, len(mock_resp.text.call_args_list))
        expected_calls = [
            mock.call('https://example.com/0'),
            mock.call('https://example.com/1'),
            mock.call('https://example.com/2')
        ]
        self.assertEqual(expected_calls, mock_session.call_args_list)
