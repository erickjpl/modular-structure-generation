from src.shared.domain.exceptions.domain_exception import HTTP_408_REQUEST_TIMEOUT
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class RequestTimeoutException(BaseAPIException):
  _api_status_code = HTTP_408_REQUEST_TIMEOUT
  _api_code = "Request Timeout Exception"
  _api_detail = "Su solicitud ha tardado demasiado en responder. Esto podría deberse a una conexión lenta o a un problema temporal con el servidor. Por favor, inténtelo de nuevo en unos minutos."
