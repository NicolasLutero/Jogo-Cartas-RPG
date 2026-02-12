from src.application.UsuarioService import UsuarioService
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

        cartas_vo = CartaDAO().buscar_por_usuario_filtrado(id_usuario, tipos)

        # Converte VO -> dict
        return [carta.to_dict() for carta in cartas_vo]

    # -----------------------------
    # CACHE (opcional futuro)
    # -----------------------------
    def limpar_cache_usuario(self, nome_usuario: str):
        if nome_usuario in self._cache:
            del self._cache[nome_usuario]
