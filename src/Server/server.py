import os
import socket

from Models.tcp_request import TcpRequest
from Server.Pool.thread_pool import ThreadPool


class HTTPServer:
    HOST = "127.0.0.1"
    PORT = int(os.getenv("API_PORT")) if os.getenv("API_PORT") is not None else 8080
    pool: ThreadPool

    def __init__(self, workers_pool: ThreadPool) -> None:  # noqa: F821
        self.pool = workers_pool
        self.init_server()

    def init_server(self) -> None:
        print(f">> Server listening on {self.HOST}:{self.PORT}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # server_socket.setblocking(False)
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen(self.pool.get_backlog_length())

            while True:  # this line didn't exist
                # gets client request
                client_socket, address = server_socket.accept()
                client_socket.setblocking(False)
                # adds client request to request pool
                self.pool.enqueue_request(TcpRequest(address, client_socket))
