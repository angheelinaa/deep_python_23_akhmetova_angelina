import argparse
import asyncio
import json
from re import sub
from collections import Counter
import aiofiles
import aiohttp
from bs4 import BeautifulSoup


def command_line_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=int)
    parser.add_argument("filename", type=str)
    return parser


async def url_parser(url, resp):
    data = await resp.text()
    parser_data = BeautifulSoup(data, "html.parser")
    lst_words = sub(r"[\W_]+", ' ', parser_data.get_text().lower()).split()
    common_words = dict(Counter(lst_words).most_common(4))
    print(f"{url}: {json.dumps(common_words, ensure_ascii=False)}")


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception
            await url_parser(url, resp)


async def fetch_worker(que):
    while True:
        url = await que.get()

        try:
            await fetch_url(url)
        except Exception:
            print(f"url '{url}' not found")
        finally:
            que.task_done()


async def batch_fetch(number, filename):
    que = asyncio.Queue(maxsize=number)

    workers = [
        asyncio.create_task(fetch_worker(que))
        for _ in range(number)
    ]

    async with aiofiles.open(filename, 'r', encoding='UTF-8') as file:
        async for url in file:
            await que.put(url.strip())

    await que.join()

    for worker in workers:
        worker.cancel()


if __name__ == "__main__":
    parser_args = command_line_parser()
    args = parser_args.parse_args()
    asyncio.run(batch_fetch(args.c, args.filename))
