import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from {{ project_name }} import settings
from src.shared.infrastructure.api.exceptions.exceptions import BaseAPIException

logger = logging.getLogger(__name__)
HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_500_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR


class ExceptionMixin:
  def handle_exception(self, exc):
    print(f"ExceptionMixin interceptó: {exc.__class__.__name__}")

    if isinstance(exc, BaseAPIException):
      logger.error(exc)
      return self._format_custom_exception_response(exc)

    context = self.get_exception_handler_context()
    response = exception_handler(exc, context)
    logger.exception(exc)

    if response is not None:
      return self._format_drf_exception_response(exc, response)

    return self._format_unexpected_error_response(exc)

  def _format_custom_exception_response(self, exc: BaseAPIException) -> Response:
    return Response(
      {
        "success": False,
        "message": exc.default_detail,
        "data": None,
        "error": {
          "code": exc.status_code,
          "type": exc.__class__.__name__,
          "details": exc.detail,
          # "extra": exc.extra_data,
        },
      },
      status=exc.status_code,
    )

  def _format_drf_exception_response(self, exc: Exception, response: Response) -> Response:
    error_detail = {
      "code": response.status_code,
      "type": exc.__class__.__name__.replace("Exception", ""),
      "details": getattr(exc, "detail", str(exc)),
      "extra": None,
    }

    if response.status_code == HTTP_400_BAD_REQUEST and isinstance(response.data, dict):
      error_detail.update(
        {
          "type": "ValidationError",
          "details": "Invalid input data.",
          "extra": response.data,
        }
      )

    return Response(
      {
        "success": False,
        "message": "Error processing request.",
        "data": None,
        "error": error_detail,
      },
      status=response.status_code,
    )

  def _format_unexpected_error_response(self, exc: Exception) -> Response:
    error_detail = {
      "code": HTTP_500_INTERNAL_SERVER_ERROR,
      "type": "InternalServerError",
      "details": "An unexpected error occurred",
      "extra": {
        "exception": str(exc),
        "type": exc.__class__.__name__,
      }
      if str(exc)
      else None,
    }

    if not settings.DEBUG:
      error_detail["details"] = "Internal server error"
      error_detail["extra"] = None

    return Response(
      {
        "success": False,
        "message": "An unexpected error occurred.",
        "data": None,
        "error": error_detail,
      },
      status=HTTP_500_INTERNAL_SERVER_ERROR,
    )
