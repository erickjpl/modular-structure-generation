from rest_framework.exceptions import APIException

from src.shared.domain.exceptions.domain_exception import HTTP_500_INTERNAL_SERVER_ERROR, DomainException


class BaseAPIException(DomainException, APIException):
  _api_status_code = HTTP_500_INTERNAL_SERVER_ERROR
  _api_code = "unexpected_error"
  _api_detail = "An unexpected error occurred."

  def __init__(self, detail: str | None = None, code: str | None = None, extra: dict | None = None):
    final_detail = detail if detail is not None else self._api_detail
    final_code = code if code is not None else self._api_code
    final_status_code = self._api_status_code

    super().__init__(
      detail=final_detail,
      status_code=final_status_code,
      default_message=final_code,
      extra_data=extra,
    )
