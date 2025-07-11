from src.shared.domain.exceptions.domain_exception import HTTP_400_BAD_REQUEST
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class BadRequestException(BaseAPIException):
  _api_status_code = HTTP_400_BAD_REQUEST
  _api_code = "bad_request"
  _api_detail = "You do not have permission to perform this action."
