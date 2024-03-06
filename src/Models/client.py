class Client:
    id_cliente: int
    saldo: int
    limite: int

    def __init__(self, id_cliente: int = 0, saldo: int = 0, limite: int = 0):
        self.id_cliente = id_cliente
        self.saldo = saldo
        self.limite = limite

    def to_string(self) -> str:
        return (
            f">> ID: {self.id_cliente}\n"
            + f">> Balance: {self.saldo}\n"
            + f">> Limit: {self.limite}"
            + f">> Invalid? {self.is_invalid()}"
        )

    def is_invalid(self) -> bool:
        return self.id_cliente not in [1, 2, 3, 4, 5]
