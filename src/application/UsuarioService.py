from src.domain.service.CartaService import CartaService
from src.domain.entity.UsuarioEntity import UsuarioEntity
from src.infra.dao.CartaDAO import CartaDAO
from src.infra.dao.UsuarioDAO import UsuarioDAO

from datetime import date


class UsuarioService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._usuarios = []
            cls._cache = {}
        return cls._instance

    # -----------------------------
    # CREATE
    # -----------------------------
    def criar_usuario(self, usuario_dict: dict) -> None:
        nome = usuario_dict["nome"]
        senha = usuario_dict["senha"]

        usuario = UsuarioEntity(None, nome, senha, None, None, None, None)
        UsuarioDAO().criar(usuario)
        self._cache[usuario.get_nome()] = usuario

    # -----------------------------
    # READ (EXISTS)
    # -----------------------------
    def usuario_existe(self, nome: str) -> bool:
        if nome in self._cache:
            return True
        usuario = UsuarioDAO().buscar_por_nome(nome)
        if usuario:
            self._cache[nome] = usuario
            return True
        return False

    # -----------------------------
    # READ (VALIDAR LOGIN)
    # -----------------------------
    def validar_login(self, nome: str, senha_hash: str) -> bool:
        if nome in self._cache:
            usuario = self._cache[nome]
        else:
            usuario = UsuarioDAO().buscar_por_nome(nome)
            if usuario:
                self._cache[nome] = usuario

        if not usuario:
            return False

        return usuario.get_senha() == senha_hash

    # -----------------------------
    # READ (ONE)
    # -----------------------------
    def buscar_usuario_dict(self, nome: str) -> dict | None:
        if nome in self._cache:
            return self._cache[nome].to_dict()
        usuario = UsuarioDAO().buscar_por_nome(nome)
        if usuario:
            self._cache[nome] = usuario
            return usuario.to_dict()
        return None

    # -----------------------------
    # UPDATE (opcional futuramente)
    # -----------------------------
    def atualizar_usuario(self, usuario_dict: dict) -> bool:
        usuario = UsuarioEntity.from_dict(usuario_dict)
        ok = UsuarioDAO().atualizar(usuario)
        if ok:
            self._cache[usuario.get_nome()] = usuario
        return ok

    # --------------------------
    # VERIFICA AÇÕES DISPONIVEIS
    # --------------------------
    def acoes_disponiveis(self, nome):
        hoje = str(date.today())

        usuario = self.buscar_usuario_dict(nome)

        if not usuario:
            return False

        # Datas vindas do banco
        data_reforjar = usuario.get("data_reforjar")
        data_cartas = usuario.get("data_cartas_diarias")
        data_fundir = usuario.get("data_fundir")

        status = {
            "reforjar": (data_reforjar != hoje),
            "cartas_diarias": (data_cartas != hoje),
            "fundir": (data_fundir != hoje)
        }

        return status

    # -------------------------
    # MARCA AÇÃO COMO REALIZADA
    # -------------------------
    def marcar_acao(self, nome, acao):
        hoje = date.today()

        # Busca usuário no banco
        usuario = self.buscar_usuario_dict(nome)

        if not usuario:
            return "Usuario não encontrado"

        # Atualiza campo correto
        if acao == "reforjar":
            usuario["data_reforjar"] = hoje
        elif acao == "cartas_diarias":
            usuario["data_cartas_diarias"] = hoje
        elif acao == "fundicao":
            usuario["data_fundir"] = hoje
        else:
            return "Ação inválida"

        # Persiste no banco
        self.atualizar_usuario(usuario)
        return True

    # -------------------------
    # COLETAR CARTAS
    # -------------------------
    def coletar_cartas(self, nome):
        usuario = UsuarioDAO().buscar_por_nome(nome)

        cartas = [CartaService().carta_aleatoria(usuario.get_id(), usuario.get_fator_n()) for _ in range(5)]
        for carta in cartas:
            CartaDAO().criar(carta)
        self.marcar_acao(nome, "cartas_diarias")

        return [carta.to_dict() for carta in cartas]
