import os
import socket

import gevent
from gevent.monkey import patch_all

from Models.tcp_request import TcpRequest
from Server.request_handler import RequestHandler

patch_all()


class HTTPServer:
    HOST: str
    PORT: int
    MAX_CONNECTIONS: int
    request_handler: RequestHandler

    def __init__(self):
        self.MAX_CONNECTIONS = (
            int(os.getenv("MAX_CONNECTIONS"))
            if os.getenv("MAX_CONNECTIONS") is not None
            else 0
        )
        self.HOST = (
            os.getenv("API_HOSTNAME")
            if os.getenv("API_HOSTNAME") is not None
            else "localhost"
        )
        self.PORT = (
            int(os.getenv("API_PORT")) if os.getenv("API_PORT") is not None else 8080
        )
        self.request_handler = RequestHandler()

    def init_server(self) -> None:
        print(f">> Server listening to port {self.PORT}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # server_socket.setblocking(False)
            server_socket.bind((self.HOST, self.PORT))
            server_socket.listen(self.MAX_CONNECTIONS)

            while True:
                client_socket, address = server_socket.accept()
                client_socket.setblocking(False)

                gevent.spawn(
                    self.request_handler.handle_client, TcpRequest(address, client_socket)
                )
