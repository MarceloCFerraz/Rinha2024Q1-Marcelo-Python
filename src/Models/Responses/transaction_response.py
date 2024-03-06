class TransactionResponse:
    saldo: int
    limite: int

    def __init__(self, sal: int, lim: int) -> None:
        self.saldo = sal
        self.limite = lim
