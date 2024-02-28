import uuid

import gevent


class TcpRequest:
    request_id: str
    address: str
    socket: gevent._socket3.socket

    def __init__(self, adr, socket) -> None:
        self.request_id = str(uuid.uuid4())
        self.address = adr
        self.socket = socket
