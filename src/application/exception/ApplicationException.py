# ApplicationException.py
class UsuarioJaExisteException(Exception):
    def __init__(self):
        super().__init__("Usuário já existe.")

class LoginRecusadoException(Exception):
    def __init__(self):
        super().__init__("Login Recusado.")

class AcaoJaFoiUsadaHojeException(Exception):
    def __init__(self, acao):
        super().__init__(f"Ação {acao} já foi usada hoje.")

class CartaNaoPertenceAOUsuarioException(Exception):
    def __init__(self):
        super().__init__(f"Carta não pertence ao usuário.")
