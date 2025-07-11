from src.shared.domain.exceptions.domain_exception import HTTP_500_INTERNAL_SERVER_ERROR
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class InternalServerErrorException(BaseAPIException):
  _api_status_code = HTTP_500_INTERNAL_SERVER_ERROR
  _api_code = "internal_server_error"
  _api_detail = "An unexpected internal server error occurred."
