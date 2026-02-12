# UsuarioEntity.py
from datetime import date
from random import random


class UsuarioEntity:
    def __init__(
        self,
        cod: int,
        nome: str,
        senha_hash: str,
        fator_n: float | None = random(),
        data_reforjar: date | None = None,
        data_cartas_diarias: date | None = None,
        data_fundir: date | None = None
    ):
        self._cod = cod
        self._nome = nome
        self._senha = senha_hash
        self._fator_n = fator_n if fator_n is not None else random()
        self._data_reforjar = data_reforjar
        self._data_cartas_diarias = data_cartas_diarias
        self._data_fundir = data_fundir

    # -------- GETTERS --------
    def get_id(self):
        return self._cod

    def get_nome(self):
        return self._nome

    def get_senha(self):
        return self._senha

    def get_fator_n(self):
        return self._fator_n

    def get_data_reforjar(self):
        return self._data_reforjar

    def get_data_cartas_diarias(self):
        return self._data_cartas_diarias

    def get_data_fundir(self):
        return self._data_fundir

    # -------- SETTERS --------
    def set_id(self, cod: str):
        self._cod = cod

    def set_nome(self, nome: str):
        self._nome = nome

    def set_senha(self, senha_hash: str):
        self._senha = senha_hash

    def set_data_reforjar(self, data: date):
        self._data_reforjar = data

    def set_data_cartas_diarias(self, data: date):
        self._data_cartas_diarias = data

    def set_data_fundir(self, data: date):
        self._data_fundir = data

    # -------- SERIALIZAÇÃO --------
    def to_dict(self) -> dict:
        return {
            "id": self._cod,
            "nome": self._nome,
            "senha": self._senha,
            "fator_n": self._fator_n,
            "data_reforjar": self._data_reforjar.isoformat() if self._data_reforjar else None,
            "data_cartas_diarias": self._data_cartas_diarias.isoformat() if self._data_cartas_diarias else None,
            "data_fundir": self._data_fundir.isoformat() if self._data_fundir else None
        }

    @staticmethod
    def from_dict(dados: dict) -> "UsuarioEntity":
        cod = dados["id"]
        nome = dados["nome"]
        senha = dados["senha"]
        fator_n = dados["fator_n"]

        data_reforjar = dados.get("data_reforjar")
        data_cartas_diarias = dados.get("data_cartas_diarias")
        data_fundir = dados.get("data_fundir")

        return UsuarioEntity(
            cod,
            nome,
            senha,
            fator_n,
            data_reforjar,
            data_cartas_diarias,
            data_fundir
        )
