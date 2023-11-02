import socket
import sys
from concurrent.futures import ThreadPoolExecutor


HOST = "127.0.0.1"
PORT = 8000


def handle(url):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(url.encode())
        resp = client_socket.recv(1024)
        print(f"{url}: {resp.decode()}")


def run_client(threads, filename):

    with ThreadPoolExecutor(max_workers=threads) as pool:
        with open(filename, "r", encoding='utf-8') as file:
            for url in file:
                pool.submit(handle, url.strip())


if __name__ == '__main__':
    run_client(int(sys.argv[1]), sys.argv[2])
