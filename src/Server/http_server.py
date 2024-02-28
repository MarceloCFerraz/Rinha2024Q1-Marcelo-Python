import os
import socket

from Pool.thread_pool import ThreadPool


class HTTPServer:
    HOST = "127.0.0.1"
    PORT = int(os.getenv("API_PORT")) if os.getenv("API_PORT") is not None else 8080
    pool: ThreadPool

    def __init__(self, workers_pool: ThreadPool) -> None:  # noqa: F821
        self.pool = workers_pool
        self.init_server()

    def init_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen(self.pool.get_backlog_length())

            print(f"Server listening on {self.HOST}:{self.PORT}")

            while True:
                client_socket, address = server_socket.accept()
                print(f"New connection: {address}. Socket: {client_socket}")
                # TODO: parse and validate request (register endpoints, check for content type, etc)
                # TODO: send request to controller (let controller handle or delegate business logic)
                print()

                client_socket.close()
