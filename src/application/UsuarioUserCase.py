# UsuarioUserCase.py
from src.domain.entity.UsuarioEntity import UsuarioEntity
from src.infra.dao.UsuarioDAO import UsuarioDAO

from datetime import date

# Exceções
from src.application.exception.ApplicationException import *


class UsuarioUserCase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._usuarios = []
            cls._cache = {}
        return cls._instance

    # -------------------------------------------
    # AUXILIAR
    # -------------------------------------------
    def buscar_usuario(self, nome: str) -> UsuarioEntity | None:
        if nome not in self._cache.keys():
            self._cache[nome] = UsuarioDAO().buscar_por_nome(nome)
        return self._cache[nome]

    def verifica_status(self, nome, campos):
        status = self.acoes_disponiveis(nome)

        for campo in campos:
            if not status[campo]:
                raise AcaoJaFoiUsadaHojeException(campo)

    # -----------------------------
    # CREATE
    # -----------------------------
    def criar_usuario(self, nome: str, senha: str) -> None:
        try:
            self.usuario_existe(nome)
            raise UsuarioJaExisteException()
        except Exception:
            usuario = UsuarioEntity(None, nome, senha, None, None, None, None)
            UsuarioDAO().criar(usuario)
            self._cache[nome] = usuario

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
            raise LoginRecusadoException()

        return usuario.get_senha() == senha_hash

    # -----------------------------
    # UPDATE (opcional futuramente)
    # -----------------------------
    def atualizar_usuario(self, usuario: UsuarioEntity) -> bool:
        ok = UsuarioDAO().atualizar(usuario)
        if ok:
            self._cache[usuario.get_nome()] = usuario
        return ok

    # --------------------------
    # VERIFICA AÇÕES DISPONIVEIS
    # --------------------------
    def acoes_disponiveis(self, nome):
        hoje = str(date.today())
        usuario = self.buscar_usuario(nome)

        data_reforjar = usuario.get_data_reforjar()
        data_cartas = usuario.get_data_cartas_diarias()
        data_fundir = usuario.get_data_fundir()

        status = {
            "reforjar": (data_reforjar != hoje),
            "cartas_diarias": (data_cartas != hoje),
            "fundir": (data_fundir != hoje)
        }

        return status

    # -------------------------
    # MARCA AÇÃO COMO REALIZADA
    # -------------------------
    def marcar_acao(self, nome, acoes):
        hoje = str(date.today())

        usuario = self.buscar_usuario(nome)

        if "reforjar" in acoes:
            usuario.set_data_reforjar(hoje)
        if "cartas_diarias" in acoes:
            usuario.set_data_cartas_diarias(hoje)
        if "fundicao" in acoes:
            usuario.set_data_fundir(hoje)

        # Persiste no banco
        self.atualizar_usuario(usuario)
        return True
