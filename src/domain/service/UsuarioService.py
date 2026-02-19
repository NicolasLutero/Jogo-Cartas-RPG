# UsuarioService.py
from datetime import date
from random import random

# Domain Class
from src.domain.entity.UsuarioEntity import UsuarioEntity

# Infra Class
from src.infra.dao.UsuarioDAO import UsuarioDAO
from src.infra.dao.CartaDAO import CartaDAO

# Exception
from src.domain.exception.DomainException import *


class UsuarioService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._cache = {}
            cls.usuario_dao = UsuarioDAO()
            cls.carta_dao = CartaDAO()
        return cls._instance


    # -------------------------------------------
    # BUSCA O USUÁRIO PELO NOME
    # -------------------------------------------
    def buscar_usuario(self, nome: str) -> UsuarioEntity | None:
        if nome not in self._cache.keys():
            self._cache[nome] = self.usuario_dao.buscar_por_nome(nome)
        return self._cache[nome]


    # -------------------------------------------
    # VERIFICANDO EXISTENCIA DO NOME
    # -------------------------------------------
    def usuario_existe(self, nome: str):
        if nome in self._cache.keys():
            return True
        usuario = self.usuario_dao.buscar_por_nome(nome)
        if usuario is not None:
            self._cache[nome] = usuario
            return True
        return False


    # -------------------------------------------
    # CRIA O OBJETO USUÁRIO
    # -------------------------------------------
    @staticmethod
    def criar_usuario(nome, senha):
        return UsuarioEntity(
            None, nome, senha,
            random(),
            None, None, None
        )


    # -------------------------------------------
    # SALVANDO OBJETO USUÁRIO
    # -------------------------------------------
    def salvar_usuario(self, usuario):
        self.usuario_dao.criar(usuario)


    # -------------------------------------------
    # LISTAR TIPOS DE CARTAS
    # -------------------------------------------
    def listar_tipos(self, usuario):
        id_dono = usuario.get_id()
        return {
            "fundos": self.carta_dao.listar_tipos(id_dono, "fundo"),
            "personagens": self.carta_dao.listar_tipos(id_dono, "personagem"),
            "bordas": self.carta_dao.listar_tipos(id_dono, "borda")
        }


    # -------------------------------------------
    # BUSCAR CARTAS DO USUÁRIO COM FILTRO
    # -------------------------------------------
    def buscar_cartas_filtrado(self, id_usuario, tipos):
        return self.carta_dao.buscar_por_usuario_filtrado(id_usuario, tipos)


    # -------------------------------------------
    # VERIFICA QUAIS AÇÕES O USUÁRIO AINDA PODE REALIZAR
    # -------------------------------------------
    @staticmethod
    def acoes_disponiveis(usuario):
        hoje = str(date.today())

        data_reforjar = usuario.get_data_reforjar()
        data_cartas = usuario.get_data_cartas_diarias()
        data_fundir = usuario.get_data_fundir()

        return {
            "reforjar": (data_reforjar != hoje),
            "cartas_diarias": (data_cartas != hoje),
            "fundir": (data_fundir != hoje)
        }


    # -------------------------------------------
    # VERIFICANDO STATUS
    # -------------------------------------------
    def verifica_status(self, usuario, campos):
        status = self.acoes_disponiveis(usuario)

        for campo in campos:
            if not status[campo]:
                raise AcaoJaFoiUsadaHojeException(campo)


    # -------------------------
    # MARCA AÇÃO COMO REALIZADA
    # -------------------------
    def marcar_acao(self, usuario, acoes):
        hoje = str(date.today())

        if "reforjar" in acoes:
            usuario.set_data_reforjar(hoje)
        if "cartas_diarias" in acoes:
            usuario.set_data_cartas_diarias(hoje)
        if "fundicao" in acoes:
            usuario.set_data_fundir(hoje)

        # Persiste no banco
        self.atualizar_usuario(usuario)


    # -------------------------------------------
    # ATUALIZAÇÃO DE USUÁRIO
    # -------------------------------------------
    def atualizar_usuario(self, usuario: UsuarioEntity) -> bool:
        ok = self.usuario_dao.atualizar(usuario)
        if ok:
            self._cache[usuario.get_nome()] = usuario
        return ok
