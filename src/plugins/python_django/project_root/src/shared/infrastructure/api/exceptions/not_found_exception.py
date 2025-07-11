from src.shared.domain.exceptions.domain_exception import HTTP_404_NOT_FOUND
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class NotFoundException(BaseAPIException):
  _api_status_code = HTTP_404_NOT_FOUND
  _api_code = "not_found"
  _api_detail = "The requested resource was not found."
