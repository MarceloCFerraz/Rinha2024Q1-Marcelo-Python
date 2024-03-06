from gevent import monkey

from Models.client import Client
from Models.transaction import Transaction

monkey.patch_all()  # Ensure monkeypatching


class ApiController:
    def __init__(self) -> None:
        pass

    def get_extrato(self, client_id: int):
        # print(f"New GET request for client {client_id}")
        client = Client(id_cliente=client_id)

        if client.is_invalid():
            return None

        print("GET transaction accepted!")

    def post_transaction(self, client_id: int, transaction: Transaction):
        # print(f"New POST request for client {client_id}")
        # print(f"Body:\n{transaction.to_string()}")

        client = Client(id_cliente=client_id)

        if transaction.is_invalid() or client.is_invalid():
            return None

        transaction.id_cliente = client_id
        print("POST transaction accepted!")
