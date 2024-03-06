import json

from gevent import monkey
from gevent.socket import wait_read

from Controllers.controller import ApiController
from Models.tcp_request import ParsedRequest, TcpRequest

monkey.patch_all()


class RequestHandler:
    controller: ApiController

    def __init__(self) -> None:
        self.controller = ApiController()

    def handle_client(self, req: TcpRequest):
        with req.socket as client_socket:
            wait_read(fileno=client_socket.fileno())  # Gevent magic
            req_bytes = client_socket.recv(1024)

            # manually parsing the request
            req.parse_request(req_bytes)
            status_code, response = self.process_request(req.parsed_request)
            status_line: str = (
                f"HTTP/1.1 {status_code} {self.get_status_name(status_code)}\r\n"
            )

            bytes_response = json.dumps(response)
            http_response = (
                status_line.encode("utf-8"),  # Status line: HTTP version, 200 Success
                b"Content-Type: application/json\r\n"  # For pickled data
                b"Content-Length: " + str(len(bytes_response)).encode() + b"\r\n"
                b"\r\n"  # Blank line separates headers and body
                 + bytes_response.encode(),
            )

            # print(http_response)

            for chunk in http_response:
                req.socket.sendall(chunk)

            del bytes_response
            del http_response
            del status_line, status_code, response, req_bytes

        del req  # freeing some memory

    def process_request(self, req: ParsedRequest):
        if req.header.method == "POST":
            if req.body is not None:
                return self.controller.post_transaction(
                    client_id=req.header.route_param, transaction=req.body
                )
            else:
                # return a 500 response because the user has not passed a body in a POST request
                pass
        elif req.header.method == "GET":
            return self.controller.get_extrato(client_id=req.header.route_param)

    def get_status_name(self, status_code: int):
        match status_code:
            case 200:
                return "OK"
            case 422:
                return "Unprocessable Entity"
            case _:
                return "Internal Server Error"
