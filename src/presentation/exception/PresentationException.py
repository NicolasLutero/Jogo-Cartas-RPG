# PresentationException.py
class DadosInvalidosException(Exception):
    def __init__(self):
        super().__init__("Dados inválidos.")

class DadosFaltantesException(Exception):
    def __init__(self):
        super().__init__("Dados obrigatórios ausentes.")

class UsuarioNaoAutentificadoException(Exception):
    def __init__(self):
        super().__init__("Usuário não autentificado.")
