from Controllers.controller import ApiController
from gevent import monkey
from gevent.socket import wait_read
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
            response = self.process_request(req.parsed_request)

            print(response)

            # request.socket.send(response)

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
