from Models.Client import Client
from Models.Transaction import Transaction


class ApiController:
    def get_extrato(client_id: int):
        client = Client(id=client_id)

        if client.is_invalid:
            return None

    def post_transaction(client_id: int):
        transaction = Transaction(id_cliente=client_id)

        if transaction.is_invalid:
            return None
