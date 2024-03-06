from datetime import datetime

from Models.transaction import Transaction


class ExtratoData:
    total: int
    data_extrato: datetime
    limite: int

    def __init__(self, total: int, data_extrato: datetime, limite: int) -> None:
        self.total = total
        self.data_extrato = data_extrato
        self.limite = limite


class ExtratoResponse:
    saldo: ExtratoData
    ultimas_transacoes: list[Transaction]

    def __init__(
        self,
        saldo: int,
        data_extrato: datetime,
        limite: int,
        ultimas_transacoes: list[Transaction],
    ) -> None:
        self.saldo = ExtratoData(saldo, data_extrato, limite)
        self.ultimas_transacoes = ultimas_transacoes
