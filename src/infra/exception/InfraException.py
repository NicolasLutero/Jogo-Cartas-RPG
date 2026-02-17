# InfraException.py
class CartaNaoEncontradaException(Exception):
    def __init__(self):
        super().__init__("Carta não encontrada")

class UsuarioNaoEncontradoException(Exception):
    def __init__(self):
        super().__init__("Usuario não encontrada")
