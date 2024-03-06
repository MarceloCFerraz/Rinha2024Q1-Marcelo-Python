import uuid
from json import JSONDecodeError, loads

from Models.transaction import Transaction


class ParsedHeader:
    method: str
    full_path: str
    base_route: str
    route_param: int
    endpoint: str
    http_version: str

    def __init__(self, method: str, full_path: str, http_v: str) -> None:
        self.method = method
        self.full_path = full_path

        if full_path[0] == "/":
            full_path = full_path[1:]  # ignores the first '/'

        path_list = full_path.split("/")

        self.base_route = path_list[0]
        self.route_param = int(path_list[1])
        self.endpoint = path_list[2]

        self.http_version = http_v


class ParsedRequest:
    header: ParsedHeader
    body: Transaction | None
    # the server will only receive a new transaction in request bodies and only
    # not sure how frameworks do to dynamically identify custom types before it reaches to controller

    def __init__(
        self, method: str, path: str, http_v: str, body: Transaction | None
    ) -> None:
        self.header = ParsedHeader(method, path, http_v)
        self.body = body


class TcpRequest:
    request_id: str
    address: str
    socket: object
    parsed_request: ParsedRequest

    def __init__(self, adr, socket) -> None:
        self.request_id = str(uuid.uuid4())
        self.address = adr
        self.socket = socket

    def parse_request(self, req_bytes: bytes):
        # b'GET /clientes/1/extrato HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/8.6.0\r\nAccept: */*\r\nContent-Type: application/json\r\n\r\n'
        # b'GET /clientes/1/extrato HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/8.6.0\r\nAccept: */*\r\n\r\n'
        # b'POST /clientes/1/transacoes HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/8.6.0\r\nAccept: */*\r\nContent-Type: application/json\r\nContent-Length: 49\r\n\r\n{"valor":100000, "tipo": "d", "descricao":"test"}'
        # b'POST /clientes/1/transacoes HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent: curl/8.6.0\r\nAccept: */*\r\nContent-Length: 49\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{"valor":100000, "tipo": "d", "descricao":"test"}'
        req_lines = str(req_bytes.decode()).splitlines()
        # req_lines = [
        #     'POST /clientes/1/transacoes HTTP/1.1',
        #     'Host: localhost:8080',
        #     'User-Agent: curl/8.6.0',
        #     'Accept: */*',
        #     'Content-Type: application/json',
        #     'Content-Length: 49',
        #     '',
        #     '{"valor":100000, "tipo": "d", "descricao":"test"}'
        # ]
        # or
        # [
        #     "GET /clientes/1/extrato HTTP/1.1",
        #     "Host: localhost:8080",
        #     "User-Agent: curl/8.6.0",
        #     "Accept: */*",
        #     "",
        # ]

        first_line = req_lines[0].split(" ")
        # first_line = ['POST', '/clientes/1/transacoes', 'HTTP/1.1']

        method = first_line[0]
        full_path = first_line[1]
        http_version = first_line[2]

        body = req_lines[len(req_lines) - 1]  # last line is reserved for the body
        try:
            body = loads(body)
            if "valor" in body.keys():
                body = Transaction.from_dict(body)

        except JSONDecodeError:
            # if the body is not parseable, probably there isn't a body
            body = None

        self.parsed_request = ParsedRequest(method, full_path, http_version, body)
