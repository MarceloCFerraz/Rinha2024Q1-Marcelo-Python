import uuid


class TcpRequest:
    request_id: str
    address: str
    socket: object

    def __init__(self, adr, socket) -> None:
        self.request_id = str(uuid.uuid4())
        self.address = adr
        self.socket = socket
