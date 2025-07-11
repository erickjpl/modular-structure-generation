from src.shared.domain.exceptions.domain_exception import (
  HTTP_500_INTERNAL_SERVER_ERROR,
  HTTP_502_BAD_GATEWAY,
  DomainException,
)
from src.shared.infrastructure.api.exceptions.exceptions import APIException, BaseAPIException


class SomeSpecificAPIError(BaseAPIException):
  _api_status_code = HTTP_502_BAD_GATEWAY
  _api_detail = "The upstream server did not respond in time."


class TestBaseAPIException:
  def test_base_api_exception_inherits_from_domain_exception(self):
    exc = BaseAPIException()

    assert isinstance(exc, APIException)
    assert isinstance(exc, DomainException)
    assert isinstance(exc, Exception)

  def test_base_api_exception_uses_defaults(self):
    exc = BaseAPIException()

    assert exc.detail == "An unexpected error occurred."
    assert exc.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.default_message == "unexpected_error"
    assert exc.extra_data == {}
    assert str(exc) == "An unexpected error occurred."

  def test_base_api_exception_with_custom_values(self):
    custom_detail = "Custom error detail"
    custom_code = "custom_error_type"
    custom_extra = {"info": "some_value"}

    exc = BaseAPIException(detail=custom_detail, code=custom_code, extra=custom_extra)

    assert exc.detail == custom_detail
    assert exc.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    assert exc.default_message == custom_code
    assert exc.extra_data == custom_extra
    assert str(exc) == custom_detail

  def test_base_api_exception_to_dict_method(self):
    exc = BaseAPIException(detail="Test detail", code="test_code", extra={"id": 123})

    exc_dict = exc.to_dict()

    expected_dict = {
      "detail": "Test detail",
      "status_code": 500,
      "message": "test_code",
      "extra_data": {"id": 123},
    }
    assert exc_dict == expected_dict

  def test_specific_api_error_inherits_and_uses_custom_defaults(self):
    exc = SomeSpecificAPIError()

    assert isinstance(exc, BaseAPIException)
    assert isinstance(exc, DomainException)
    assert exc.detail == "The upstream server did not respond in time."
    assert exc.status_code == HTTP_502_BAD_GATEWAY
    assert exc.default_message == "unexpected_error"
    assert exc.extra_data == {}
    assert str(exc) == "The upstream server did not respond in time."

  def test_specific_api_error_can_override_defaults(self):
    custom_detail = "Specific gateway issue"
    custom_code = "custom_gateway_error"
    custom_extra = {"upstream_service": "auth_service"}

    exc = SomeSpecificAPIError(detail=custom_detail, code=custom_code, extra=custom_extra)

    assert exc.detail == custom_detail
    assert exc.status_code == HTTP_502_BAD_GATEWAY
    assert exc.default_message == custom_code
    assert exc.extra_data == custom_extra
