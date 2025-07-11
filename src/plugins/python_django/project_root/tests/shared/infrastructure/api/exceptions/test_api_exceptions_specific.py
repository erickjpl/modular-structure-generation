from http import HTTPStatus

import pytest

from src.shared.domain.exceptions.domain_exception import (
  HTTP_401_UNAUTHORIZED,
  HTTP_403_FORBIDDEN,
  HTTP_404_NOT_FOUND,
  HTTP_405_METHOD_NOT_ALLOWED,
  HTTP_406_NOT_ACCEPTABLE,
  HTTP_408_REQUEST_TIMEOUT,
  HTTP_422_UNPROCESSABLE_ENTITY,
  HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException
from src.shared.infrastructure.api.exceptions.forbidden_exception import ForbiddenException
from src.shared.infrastructure.api.exceptions.internal_server_error_exception import InternalServerErrorException
from src.shared.infrastructure.api.exceptions.method_not_allowed_exception import MethodNotAllowedException
from src.shared.infrastructure.api.exceptions.not_acceptable_exception import NotAcceptableException
from src.shared.infrastructure.api.exceptions.not_found_exception import NotFoundException
from src.shared.infrastructure.api.exceptions.request_timeout_exception import RequestTimeoutException
from src.shared.infrastructure.api.exceptions.unauthorized_exception import UnauthorizedException
from src.shared.infrastructure.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException

API_SPECIFIC_EXCEPTIONS = [
  (ForbiddenException, HTTP_403_FORBIDDEN, "forbidden", "You do not have permission to perform this action."),
  (
    InternalServerErrorException,
    HTTP_500_INTERNAL_SERVER_ERROR,
    "internal_server_error",
    "An unexpected internal server error occurred.",
  ),
  (
    MethodNotAllowedException,
    HTTP_405_METHOD_NOT_ALLOWED,
    "method_not_allowed",
    "The action you attempted is not permitted for this resource. Please check the API documentation for permitted methods.",
  ),
  (
    NotAcceptableException,
    HTTP_406_NOT_ACCEPTABLE,
    "Not Acceptable",
    "Lo sentimos, no podemos responder a esta solicitud en el formato que ha especificado. Por favor, asegúrese de que el tipo de contenido que está solicitando sea compatible con nuestra API.",
  ),
  (NotFoundException, HTTP_404_NOT_FOUND, "not_found", "The requested resource was not found."),
  (
    RequestTimeoutException,
    HTTP_408_REQUEST_TIMEOUT,
    "Request Timeout Exception",
    "Su solicitud ha tardado demasiado en responder. Esto podría deberse a una conexión lenta o a un problema temporal con el servidor. Por favor, inténtelo de nuevo en unos minutos.",
  ),
  (
    UnauthorizedException,
    HTTP_401_UNAUTHORIZED,
    "unauthorized",
    "Authentication credentials were not provided or are invalid.",
  ),
  (
    UnprocessableEntityException,
    HTTP_422_UNPROCESSABLE_ENTITY,
    "unprocessable_entity",
    "The request was well-formed but could not be processed due to semantic errors.",
  ),
]


class TestAPISpecificExceptions:
  @pytest.mark.parametrize(
    "exception_class, expected_status_code, expected_default_code, expected_default_detail", API_SPECIFIC_EXCEPTIONS
  )
  def test_should_use_correct_default_values(
    self,
    exception_class: type[BaseAPIException],
    expected_status_code: HTTPStatus,
    expected_default_code: str,
    expected_default_detail: str,
  ):
    exception_instance = exception_class()

    assert isinstance(exception_instance, BaseAPIException)

    assert exception_instance.detail == expected_default_detail
    assert exception_instance.status_code == expected_status_code
    assert exception_instance.default_message == expected_default_code
    assert exception_instance.extra_data == {}
    assert str(exception_instance) == expected_default_detail

  @pytest.mark.parametrize(
    "exception_class, expected_status_code, expected_default_code, expected_default_detail", API_SPECIFIC_EXCEPTIONS
  )
  def test_should_allow_overriding_values(
    self,
    exception_class: type[BaseAPIException],
    expected_status_code: HTTPStatus,
    expected_default_code: str,
    expected_default_detail: str,
  ):
    custom_detail = "This is a custom message for the test."
    custom_code = "custom_error_code"
    custom_extra = {"test_key": "test_value"}

    exception_instance = exception_class(detail=custom_detail, code=custom_code, extra=custom_extra)

    assert exception_instance.detail == custom_detail
    assert exception_instance.status_code == exception_class._api_status_code
    assert exception_instance.default_message == custom_code
    assert exception_instance.extra_data == custom_extra
    assert str(exception_instance) == custom_detail

  def test_forbidden_exception_defaults(self):
    exc = ForbiddenException()
    assert exc.detail == "You do not have permission to perform this action."
    assert exc.status_code == HTTP_403_FORBIDDEN
    assert exc.default_message == "forbidden"
    assert exc.extra_data == {}
    assert str(exc) == "You do not have permission to perform this action."

  def test_not_found_exception_defaults(self):
    exc = NotFoundException()
    assert exc.detail == "The requested resource was not found."
    assert exc.status_code == HTTP_404_NOT_FOUND
    assert exc.default_message == "not_found"
    assert exc.extra_data == {}
    assert str(exc) == "The requested resource was not found."
