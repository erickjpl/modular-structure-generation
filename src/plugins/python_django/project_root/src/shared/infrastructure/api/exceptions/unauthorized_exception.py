from src.shared.domain.exceptions.domain_exception import HTTP_401_UNAUTHORIZED
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class UnauthorizedException(BaseAPIException):
  _api_status_code = HTTP_401_UNAUTHORIZED
  _api_code = "unauthorized"
  _api_detail = "Authentication credentials were not provided or are invalid."
