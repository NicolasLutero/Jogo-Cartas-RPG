# CartaEntity.py
from typing import Dict


class CartaEntity:
    def __init__(
        self,
        cod: int,
        fundo: str,
        personagem: str,
        borda: str,
        stats: Dict[str, float],
        dono: int
    ):
        self._cod = cod
        self._fundo = fundo
        self._personagem = personagem
        self._borda = borda
        self._stats = stats
        self._dono = dono

    # -------- GETTERS --------
    def get_id(self):
        return self._cod

    def get_nome(self):
        return f"{self._personagem} da {self._fundo} {self._borda}"

    def get_fundo(self):
        return self._fundo

    def get_personagem(self):
        return self._personagem

    def get_borda(self):
        return self._borda

    def get_stats(self):
        return self._stats

    def get_atributo(self, atr: str) -> float:
        return self._stats.get(atr, 0.0)

    def get_dono(self) -> int:
        return self._dono

    # -------- SETTERS --------
    def set_id(self, cod):
        self._cod = cod

    def set_cenario(self, fundo: str):
        self._fundo = fundo

    def set_personagem(self, personagem: str):
        self._personagem = personagem

    def set_raridade(self, borda: str):
        self._borda = borda

    def set_stats(self, stats: Dict[str, float]):
        self._stats = stats

    def set_atributo(self, atr: str, valor: float):
        self._stats[atr] = valor

    # -------- SERIALIZAÇÃO --------
    def to_dict(self) -> dict:
        return {
            "id": self._cod,
            "nome": self.get_nome(),
            "fundo": self._fundo,
            "personagem": self._personagem,
            "borda": self._borda,
            "stats": dict(self._stats),
            "dono": self._dono
        }

    @staticmethod
    def from_dict(dados: dict) -> "CartaEntity":
        return CartaEntity(
            dados["id"],
            dados["fundo"],
            dados["personagem"],
            dados["borda"],
            dict(dados.get("stats", {})),
            dados["dono"]
        )

    # -------- REPRESENTAÇÃO --------
    def __repr__(self):
        return (
            f"CartaEntity(nome={self.get_nome()!r}, cenario={self._fundo!r}, "
            f"personagem={self._personagem!r}, raridade={self._borda!r}, stats={self._stats!r})"
        )
