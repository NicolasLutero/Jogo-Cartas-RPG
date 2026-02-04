from datetime import date


class CartaVO:
    def __init__(self, cod):
        pass


    # -------- GETTERS --------
    def get_nome(self):
        return self._nome

    def get_senha(self):
        return self._senha

    def get_data_reforjar(self):
        return self._data_reforjar

    def get_data_cartas_diarias(self):
        return self._data_cartas_diarias

    def get_data_fundir(self):
        return self._data_fundir

    # -------- SETTERS --------
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
            "nome": self._nome,
            "senha": self._senha,
            "data_reforjar": self._data_reforjar.isoformat() if self._data_reforjar else None,
            "data_cartas_diarias": self._data_cartas_diarias.isoformat() if self._data_cartas_diarias else None,
            "data_fundir": self._data_fundir.isoformat() if self._data_fundir else None
        }

    @staticmethod
    def from_dict(dados: dict) -> "UsuarioVO":
        nome = dados["nome"]
        senha = dados["senha"]

        data_reforjar = dados.get("data_reforjar")
        data_cartas_diarias = dados.get("data_cartas_diarias")
        data_fundir = dados.get("data_fundir")

        return UsuarioVO(
            nome,
            senha,
            data_reforjar,
            data_cartas_diarias,
            data_fundir
        )
