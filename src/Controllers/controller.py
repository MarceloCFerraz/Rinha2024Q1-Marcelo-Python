from gevent import monkey

from Db.db_manager import DbManager
from Models.client import Client
from Models.transaction import Transaction

monkey.patch_all()  # Ensure monkeypatching


class ApiController:
    db_manager: DbManager

    def __init__(self) -> None:
        self.db_manager = DbManager()

    def get_extrato(self, client_id: int) -> tuple[int, object]:
        # # print(f"New GET request for client {client_id}")
        status_code = 422
        response = {}
        client = Client(id_cliente=client_id)

        if not client.is_invalid():
            del client
            # print("GET transaction accepted!")
            command = "SELECT customer_balance, customer_limit, report_date, last_transactions FROM get_client_data(%s)"
            params = (client_id,)

            rows = self.db_manager.execute_query(command, params)

            if rows is not None:
                status_code = 200
                row = rows[0]  # this endpoint always returns a single row
                response = {
                    "saldo": {
                        "total": row[0],
                        "data_extrato": row[2].strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "limite": row[1],
                    },
                    "ultimas_transacoes": row[3],
                }

                del row
            else:
                status_code = 500

            del rows

        return status_code, response

    def post_transaction(self, client_id: int, transaction: Transaction):
        # # print(f"New POST request for client {client_id}")
        # # print(f"Body:\n{transaction.to_string()}")
        status_code = 422
        response = {}

        client = Client(id_cliente=client_id)

        if not transaction.is_invalid() and not client.is_invalid():
            del client

            command = (
                "SELECT success, client_limit, new_balance from {}(%s, %s, %s)".format(
                    "debit" if transaction.tipo == "d" else "credit"
                )
            )
            params = (client_id, transaction.valor, transaction.descricao)
            rows = self.db_manager.execute_query(query=command, params=params)

            if rows is not None and rows[0][0]:  # not null and success
                status_code = 200
                response = {"limite": rows[0][1], "saldo": rows[0][2]}
        # print("POST transaction accepted!")
        return status_code, response
