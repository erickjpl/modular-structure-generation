from src.shared.domain.exceptions.domain_exception import HTTP_406_NOT_ACCEPTABLE
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class NotAcceptableException(BaseAPIException):
  _api_status_code = HTTP_406_NOT_ACCEPTABLE
  _api_code = "Not Acceptable"
  _api_detail = "Lo sentimos, no podemos responder a esta solicitud en el formato que ha especificado. Por favor, asegúrese de que el tipo de contenido que está solicitando sea compatible con nuestra API."
