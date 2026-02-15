from src.application.UsuarioService import UsuarioService
from src.domain.service.CartaService import CartaService
from src.infra.dao.CartaDAO import CartaDAO


class InventarioService:
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
        """
        Retorna lista única de tipos de personagem existentes no banco.
        Ex: ["Mago", "Arqueiro", "Guerreiro"]
        """
        usuario = UsuarioService().buscar_usuario_dict(usuario)
        id_usuario = usuario["id"]
        return CartaDAO().listar_tipos(id_usuario)

    # -----------------------------
    # BUSCAR CARTAS DO USUÁRIO
    # -----------------------------
    @staticmethod
    def buscar_cartas_usuario(usuario: str, tipos: dict) -> list[dict]:
        usuario = UsuarioService().buscar_usuario_dict(usuario)
        id_usuario = usuario["id"]

        cartas_entities = CartaDAO().buscar_por_usuario_filtrado(id_usuario, tipos)

        # Converte VO -> dict
        return [CartaService().para_client(carta) for carta in cartas_entities]

    @staticmethod
    def buscar_carta_usuario(usuario: str, id_carta: int) -> dict:
        usuario = UsuarioService().buscar_usuario_dict(usuario)
        id_usuario = usuario["id"]

        carta_entity = CartaDAO().buscar_usuario_carta(id_usuario, id_carta)

        # Converte VO -> dict
        return CartaService().para_client(carta_entity)

    # -----------------------------
    # CACHE (opcional futuro)
    # -----------------------------
    def limpar_cache_usuario(self, nome_usuario: str):
        if nome_usuario in self._cache:
            del self._cache[nome_usuario]

    # -----------------------------
    # REFORJAR CARTA
    # -----------------------------
    @staticmethod
    def reforjar_carta(nome_usuario, id_carta):
        usuario = UsuarioService().buscar_usuario_dict(nome_usuario)

        id_usuario = usuario["id"]
        carta_entity = CartaDAO().buscar_usuario_carta(id_usuario, id_carta)

        if carta_entity is not None:
            UsuarioService().marcar_acao(nome_usuario, "reforjar")
            for _ in range(1):
                carta_entity = CartaService().reforjar(usuario["fator_n"], carta_entity)
            print("OK")
            return CartaService().para_client(carta_entity)
        else:
            return None
