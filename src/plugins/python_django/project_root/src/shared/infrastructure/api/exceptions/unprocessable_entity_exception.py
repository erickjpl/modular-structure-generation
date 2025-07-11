from src.shared.domain.exceptions.domain_exception import HTTP_422_UNPROCESSABLE_ENTITY
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException


class UnprocessableEntityException(BaseAPIException):
  _api_status_code = HTTP_422_UNPROCESSABLE_ENTITY
  _api_code = "unprocessable_entity"
  _api_detail = "The request was well-formed but could not be processed due to semantic errors."
