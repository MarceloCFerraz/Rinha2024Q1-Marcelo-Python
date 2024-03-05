import json

import httptools
from Controllers.controller import ApiController
from gevent import monkey
from gevent.socket import wait_read
from Models.tcp_request import TcpRequest

monkey.patch_all()


class RequestHandler:
    controller: ApiController
    routes: dict[str]
    parser: object

    def init(self):
        self.controller = ApiController()
        self.routes = {
            "transacoes": self.controller.post_transaction,
            "extrato": self.controller.get_extrato,
        }

    def handle_client(self, req: TcpRequest):
        with req.socket as client_socket:
            # print(req)
            wait_read(fileno=client_socket.fileno())  # Gevent magic
            req_bytes = client_socket.recv(1024)

            print(self.parse_request(req_bytes))
            # data = req.socket.makefile(mode="rb").decode()
            # request.socket.close()

    def parse_request(self, request_bytes):
        headers = {}
        json_data = {}  # initialize an empty dictionary for JSON data

        def on_header(name: bytes, value: bytes):
            headers[name.decode().lower()] = value.decode()

        def on_body(body: bytes):
            body_data = body.decode()
            try:
                json_data = json.loads(body_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in request body")

        parser = httptools.HttpRequestParser(self)
        parser.feed_data(request_bytes)

        print(parser.get_method())
        print(parser.get_path())

        return (
            parser.get_method().decode(),
            parser.get_path().decode(),
            headers,
            json_data,
        )

    def extract_info(self, path):
        parts = path.split("/")[1:]  # Split the path. Ignore empty first element
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return None, None

    def handle_request(self, path: str) -> dict:
        if not path.startswith("/cliente/"):
            self.send_error(404, "Invalid path")

        client_id, operation = self.extract_info(self.path)

        try:
            self.routes[operation](client_id)
        except KeyError:
            self.send_error(404, "Invalid route")

    def do_GET(self):
        self.handle_request(self.path)

    def do_POST(self):
        self.handle_request(self.path)
