from datetime import datetime


class Transaction:
    id_cliente: int
    valor: float
    realizada_em: datetime
    tipo: chr
    descricao: str

    def __init__(
        self,
        id_cliente: int = 0,
        valor: int = 0,
        realizada_em: datetime = datetime.utcnow(),
        tipo: chr = "m",
        descricao: str = "marcelo",
    ):
        self.id_cliente = id_cliente
        self.valor = valor
        self.tipo = tipo
        self.descricao = descricao

    def to_string(self) -> str:
        return (
            f">> Client: {self.id_cliente}\n"
            + f">> Value: {self.valor}\n"
            + f">> Date: {self.realizada_em}\n"
            + f">> Type: {self.tipo}\n"
            + f">> Description: {self.descricao}"
        )

    def is_invalid(self) -> bool:
        return (
            (self.tipo != "c" and self.tipo != "d")
            or self.valor <= 0
            or self.valor % 1 != 0
            or len(self.descricao) > 10
        )
