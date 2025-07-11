from src.shared.domain.exceptions.domain_exception import HTTP_403_FORBIDDEN
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class ForbiddenException(BaseAPIException):
  _api_status_code = HTTP_403_FORBIDDEN
  _api_code = "forbidden"
  _api_detail = "You do not have permission to perform this action."
