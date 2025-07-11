from src.shared.infrastructure.api.api_response import success_response
from src.shared.infrastructure.api.exceptions.not_found_exception import NotFoundException
from src.shared.infrastructure.api.views.commad_api_view import CommandAPIView


class UpdateAPIView(CommandAPIView):
  view_name = "DestroyAPIView"

  def update(self, request, pk):
    validated_data = self._validate_request_serializer(request.data)

    command = self.application_command(validated_data)

    updated_item = self.infrastructure_command_bus.dispatch(pk, command)

    if not updated_item:
      raise NotFoundException(detail=f"Recurso con ID {pk} no encontrado para actualización.")

    return success_response(
      message=self.message_response if self.message_response is not None else f"Recurso {pk} actualizado exitosamente.",
    )

  def patch(self, request, pk):
    validated_data = self._validate_request_serializer(request.data, partial=True)

    command = self.application_command(validated_data)

    updated_item = self.infrastructure_command_bus.dispatch(pk, command)

    if not updated_item:
      raise NotFoundException(detail=f"Recurso con ID {pk} no encontrado para actualización parcial.")

    return success_response(
      message=self.message_response
      if self.message_response is not None
      else f"Recurso {pk} actualizado parcialmente exitosamente.",
    )
