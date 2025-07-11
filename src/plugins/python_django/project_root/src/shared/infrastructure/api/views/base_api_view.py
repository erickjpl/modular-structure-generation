from rest_framework.viewsets import GenericViewSet

from src.shared.infrastructure.api.exceptions.exception_handler import ExceptionMixin
from src.shared.infrastructure.api.exceptions.internal_server_error_exception import InternalServerErrorException
from src.shared.infrastructure.api.exceptions.unprocessable_entity_exception import UnprocessableEntityException


class BaseAPIView(ExceptionMixin, GenericViewSet):
  view_name = None
  repositories = None
  message_response = None
  request_serializer_class = None
  response_serializer_class = None

  def _validate_request_serializer(self, data, partial=False):
    if not self.request_serializer_class:
      raise InternalServerErrorException(detail="request_serializer_class debe ser definido para esta vista.")

    serializer = self.request_serializer_class(data=data, partial=partial)
    if not serializer.is_valid():
      raise UnprocessableEntityException(
        detail="Error de validación en los datos de entrada.",
        extra=serializer.errors,
      )

    return serializer.validated_data

  def _validate_response_serializer(self, data, many=False):
    if not self.response_serializer_class:
      raise InternalServerErrorException(detail="response_serializer_class debe ser definido para esta vista.")

    serializer = self.response_serializer_class(instance=data, many=many)

    return serializer.data
