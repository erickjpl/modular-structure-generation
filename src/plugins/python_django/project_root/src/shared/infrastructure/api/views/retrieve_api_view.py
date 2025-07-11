from django.forms import ValidationError

from src.shared.infrastructure.api.api_response import success_response
from src.shared.infrastructure.api.views.query_api_view import QueryAPIView


class RetrieveAPIView(QueryAPIView):
  view_name = "RetrieveAPIView"

  def get(self, request, pk):
    query = self.application_query(pk=pk)

    item = self.infrastructure_query_bus.ask(query)

    if item is None:
      return success_response(
        message=self.message_response if self.message_response is not None else f"Recurso {pk} no encontrado.",
        data=None,
      )

    serialized_item = self._validate_response_serializer(item).data

    return success_response(
      message=self.message_response if self.message_response is not None else f"Recurso {pk} obtenido exitosamente.",
      data=serialized_item,
    )

  def _validate_response_serializer(self, item):
    serializer = self.response_serializer_class(instance=item)
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    return serializer
