from src.shared.domain.exceptions.domain_exception import HTTP_405_METHOD_NOT_ALLOWED
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class MethodNotAllowedException(BaseAPIException):
  _api_status_code = HTTP_405_METHOD_NOT_ALLOWED
  _api_code = "method_not_allowed"
  _api_detail = "The action you attempted is not permitted for this resource. Please check the API documentation for permitted methods."
