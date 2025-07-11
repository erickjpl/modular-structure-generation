from django.forms import ValidationError
from rest_framework.mixins import ListModelMixin

from src.shared.infrastructure.api.api_response import success_response
from src.shared.infrastructure.api.views.query_api_view import QueryAPIView


class ListAPIView(QueryAPIView, ListModelMixin):
  view_name = "ListAPIView"

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def list(self, request):
    skip = int(request.query_params.get("skip", 0))
    limit = int(request.query_params.get("limit", 50))

    query = self.application_query(skip=skip, limit=limit)

    items = self.infrastructure_query_bus.ask(query)
    serialized_items = self._serialize_items(items)

    return success_response(
      message=self.message_response if self.message_response is not None else "Recursos obtenidos exitosamente.",
      data=serialized_items,
    )

  def _serialize_items(self, items):
    serializer = self.response_serializer_class(data=items, many=True)
    if not serializer.is_valid():
      raise ValidationError(serializer.errors)
    return serializer.data
