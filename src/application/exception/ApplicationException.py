# ApplicationException.py
class UsuarioJaExisteException(Exception):
    def __init__(self):
        super().__init__("Usuário já existe.")

class LoginRecusadoException(Exception):
    def __init__(self):
        super().__init__("Login Recusado.")

class UsuarioNaoExisteException(Exception):
    def __init__(self):
        super().__init__("Usuário não existe.")

class CartaNaoExisteException(Exception):
    def __init__(self):
        super().__init__("Carta não existe.")

class CartaNaoPertenceAOUsuarioException(Exception):
    def __init__(self):
        super().__init__(f"Carta não pertence ao usuário.")
