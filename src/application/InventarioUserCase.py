from src.application.UsuarioUserCase import UsuarioUserCase
from src.domain.service.CartaService import CartaService

from src.infra.dao.CartaDAO import CartaDAO

from src.application.exception.ApplicationException import *


class InventarioUserCase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._cache = {}
        return cls._instance

    # -----------------------------
    # LISTAR TIPOS DE FUNDO, PERSONAGEM E BORDA
    # -----------------------------
    @staticmethod
    def listar_tipos(usuario) -> list[str]:
        usuario = UsuarioUserCase().buscar_usuario(usuario)
        return CartaDAO().listar_tipos(usuario.get_id())

    # -----------------------------
    # BUSCAR CARTAS DO USUÁRIO
    # -----------------------------
    @staticmethod
    def buscar_cartas_usuario(usuario: str, tipos: dict) -> list[dict]:
        usuario = UsuarioUserCase().buscar_usuario(usuario)
        id_usuario = usuario.get_id()

        cartas_entities = CartaDAO().buscar_por_usuario_filtrado(id_usuario, tipos)

        # Converte VO -> dict
        return [CartaService().para_client(carta) for carta in cartas_entities]

    @staticmethod
    def buscar_carta_usuario(usuario: str, id_carta: int) -> dict:
        usuario = UsuarioUserCase().buscar_usuario(usuario)
        id_usuario = usuario.get_id()

        carta_entity = CartaDAO().buscar_usuario_carta(id_usuario, id_carta)

        # Converte VO -> dict
        return CartaService().para_client(carta_entity)

    # -----------------------------
    # COLETAR CARTAS
    # -----------------------------
    @staticmethod
    def coletar_cartas(nome):
        usuario = UsuarioUserCase().buscar_usuario(nome)

        UsuarioUserCase().verifica_status(nome, ["cartas_diarias"])

        cartas = [CartaService().carta_aleatoria(usuario.get_id(), usuario.get_fator_n()) for _ in range(5)]
        for carta in cartas:
            CartaDAO().criar(carta)

        UsuarioUserCase().marcar_acao(nome, "cartas_diarias")

        return [CartaService().para_client(carta) for carta in cartas]

    # -----------------------------
    # REFORJAR CARTA
    # -----------------------------
    @staticmethod
    def reforjar_carta(nome_usuario, id_carta):
        usuario = UsuarioUserCase().buscar_usuario(nome_usuario)

        id_usuario = usuario.get_id()
        carta_entity = CartaDAO().buscar_usuario_carta(id_usuario, id_carta)

        if carta_entity is not None:
            UsuarioUserCase().marcar_acao(nome_usuario, ["reforjar"])
            carta_entity = CartaService().reforjar(usuario.get_fator_n(), carta_entity)
            return CartaService().para_client(carta_entity)
        else:
            raise CartaNaoPertenceAOUsuarioException()
