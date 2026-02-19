# UsuarioUserCase.py
import hashlib

# Domain Class
from src.domain.service.UsuarioService import UsuarioService
from src.domain.service.CartaService import CartaService

# Exception
from src.application.exception.ApplicationException import *


class UsuarioUserCase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.usuario_service = UsuarioService()
            cls.carta_service = CartaService()
        return cls._instance

    # -------------------------------------------
    # AUZILIAR
    # -------------------------------------------
    @staticmethod
    def hash_sha256(txt: str) -> str:
        hash_txt = hashlib.sha256(txt.encode("utf-8"))
        return hash_txt.hexdigest()


    # -----------------------------
    # CREATE
    # -----------------------------
    def criar_usuario(self, nome: str, senha: str) -> None:
        senha = self.hash_sha256(senha)
        if not self.usuario_service.usuario_existe(nome):
            usuario = self.usuario_service.criar_usuario(nome, senha)
            self.usuario_service.salvar_usuario(usuario)
        else:
            raise UsuarioJaExisteException()


    # -----------------------------
    # VALIDAR LOGIN
    # -----------------------------
    def validar_login(self, nome: str, senha: str) -> bool:
        senha = self.hash_sha256(senha)
        usuario = self.usuario_service.buscar_usuario(nome)
        if not usuario or (not usuario.get_senha() == senha):
            raise LoginRecusadoException()


    # --------------------------
    # VERIFICA AÇÕES DISPONIVEIS
    # --------------------------
    def acoes_disponiveis(self, nome):
        usuario = self.usuario_service.buscar_usuario(nome)
        if not usuario:
            raise UsuarioNaoExisteException()

        status = self.usuario_service.acoes_disponiveis(usuario)
        return status
