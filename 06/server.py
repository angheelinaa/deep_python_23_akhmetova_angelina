import socket
from urllib.request import urlopen
from urllib.error import HTTPError
import argparse
from re import sub
from collections import Counter
import json
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


COUNT_URLS = [0]
lock = Lock()


def command_line_parser():
    parser_args = argparse.ArgumentParser()
    parser_args.add_argument('-w', default=1, type=int)
    parser_args.add_argument('-k', default=1, type=int)
    return parser_args


def fetch_url(url, k):
    try:
        data = urlopen(url)
    except HTTPError:
        print(f"url '{url}' not found")
        return
    parser_data = BeautifulSoup(data.read(), "html.parser")
    lst_words = sub(r"[\W_]+", ' ', parser_data.get_text().lower()).split()
    common_words = dict(Counter(lst_words).most_common(k))
    return common_words


def handle_client(client_socket, k):
    with client_socket:
        url = client_socket.recv(1024).decode()
        top_common_words = fetch_url(url, k)
        if top_common_words is None:
            resp = "url not found"
            client_socket.sendall(resp.encode())
        else:
            resp = json.dumps(top_common_words, ensure_ascii=False)
            client_socket.sendall(resp.encode())
            with lock:
                COUNT_URLS[0] += 1
                print(f"обработано урлов: {COUNT_URLS[0]}")


def run_server(workers, top_common_words):
    host = "127.0.0.1"
    port = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        server_socket.settimeout(5)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            while True:
                try:
                    client_socket, client_address = server_socket.accept()
                except TimeoutError:
                    print("timed out")
                    break
                pool.submit(handle_client, client_socket, top_common_words)


if __name__ == '__main__':
    parser = command_line_parser()
    namespace = parser.parse_args()
    run_server(namespace.w, namespace.k)
