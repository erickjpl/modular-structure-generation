from rest_framework.status import HTTP_204_NO_CONTENT

from src.shared.infrastructure.api.api_response import success_response
from src.shared.infrastructure.api.views.commad_api_view import CommandAPIView


class DestroyAPIView(CommandAPIView):
  view_name = "DestroyAPIView"

  def destroy(self, request, pk):
    command = self.application_command({"id": pk})

    self.infrastructure_command_bus.dispatch(command)

    return success_response(
      message=self.message_response if self.message_response is not None else f"Recurso {pk} eliminado exitosamente.",
      status_code=HTTP_204_NO_CONTENT,
    )
