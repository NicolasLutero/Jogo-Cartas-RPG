# HttpExceptionMapper.py
from src.application.exception.ApplicationException import *
from src.presentation.exception.PresentationException import *
from src.domain.exception.DomainException import *


class HttpException(Exception):
    def __init__(self, mensagem: str, status_code: int):
        self.status_code = status_code
        super().__init__(f"{status_code} - {mensagem}")


class HttpExceptionMapper:
    @staticmethod
    def map_http(e):
        # Presentation Exceptions
        if isinstance(e, DadosInvalidosException):
            return HttpException(str(e), 400)
        elif isinstance(e, DadosFaltantesException):
            return HttpException(str(e), 400)
        elif isinstance(e, UsuarioNaoAutentificadoException):
            return HttpException(str(e), 401)

        # Application Exceptions
        elif isinstance(e, UsuarioJaExisteException):
            return HttpException(str(e), 409)
        elif isinstance(e, LoginRecusadoException):
            return HttpException(str(e), 401)
        elif isinstance(e, UsuarioNaoExisteException):
            return HttpException(str(e), 404)
        elif isinstance(e, CartaNaoExisteException):
            return HttpException(str(e), 404)
        elif isinstance(e, CartaNaoPertenceAOUsuarioException):
            return HttpException(str(e), 404)

        # Domain Exceptions
        elif isinstance(e, AcaoJaFoiUsadaHojeException):
            return HttpException(str(e), 403)

        return None
