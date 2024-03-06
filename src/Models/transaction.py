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
        self.realizada_em = realizada_em
        self.tipo = tipo
        self.descricao = descricao

    @classmethod
    def from_dict(cls, body: dict):
        return cls(
            valor=body.get("valor"),
            tipo=body.get("tipo"),
            descricao=body.get("descricao"),
        )

    def to_string(self) -> str:
        return (
            f">> Value: {self.valor}\n"
            + f">> Date: {self.realizada_em}\n"
            + f">> Type: {self.tipo}\n"
            + f">> Description: {self.descricao}\n"
            + f">> Invalid? {self.is_invalid()}"
        )

    def is_invalid(self) -> bool:
        return (
            (self.tipo != "c" and self.tipo != "d")
            or self.valor <= 0
            or self.valor % 1 != 0  # checks if value is not an integer
            or len(self.descricao) > 10
        )
