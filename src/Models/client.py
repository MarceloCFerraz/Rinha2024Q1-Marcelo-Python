class Client:
    id: int = 0
    saldo: int = 0
    limite: int = 0

    def __init__(self, id: int = 0, saldo: int = 0, limite: int = 0):
        self.id = id
        self.saldo = saldo
        self.limite = limite

    def to_string(self) -> str:
        return (
            f">> ID: {self.id}\n"
            + f">> Balance: {self.saldo}\n"
            + f">> Limit: {self.limite}"
        )

    def is_invalid(self) -> bool:
        return self.id not in [1, 2, 3, 4, 5]
