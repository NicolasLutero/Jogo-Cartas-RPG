# DomainException.py
class AcaoJaFoiUsadaHojeException(Exception):
    def __init__(self, acao):
        super().__init__(f"Ação {acao} já foi usada hoje.")
