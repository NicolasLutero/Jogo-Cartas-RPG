# HttpExceptionMapper.py
from src.application.exception.ApplicationException import *
from src.presentation.exception.PresentationException import *
from src.domain.exception.DomainException import *
from src.infra.exception.InfraException import *


class HttpException(Exception):
    def __init__(self, mensagem: str, status_code: int):
        self.status_code = status_code
        super().__init__(mensagem)

class HttpExceptionMapper:
    @staticmethod
    def map_http(e):
        # Presentation Exceptions
            # LoginCadastroRoutes.py
        if isinstance(e, DadosInvalidosException):
            return HttpException(str(e), 400)
        elif isinstance(e, DadosFaltantesException):
            return HttpException(str(e), 400)
            # MecanicaRoutes.py
        elif isinstance(e, UsuarioNaoAutentificadoException):
            return HttpException(str(e), 401)

        # Application Exceptions
            # UsuarioUserCase.py
        elif isinstance(e, UsuarioJaExisteException):
            return HttpException(str(e), 409)
        elif isinstance(e, LoginRecusadoException):
            return HttpException(str(e), 401)
        elif isinstance(e, AcaoJaFoiUsadaHojeException):
            return HttpException(str(e), 403)
            # InventarioUserCase.py
        elif isinstance(e, CartaNaoPertenceAOUsuarioException):
            return HttpException(str(e), 404)

        # Infra Exceptions
            # CartaDAO.py
        elif isinstance(e, CartaNaoEncontradaException):
            return HttpException(str(e), 404)
            # UsuarioDAO.py
        elif isinstance(e, UsuarioNaoEncontradoException):
            return HttpException(str(e), 404)


        return None
