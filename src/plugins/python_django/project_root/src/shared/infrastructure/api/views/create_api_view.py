from src.shared.domain.exceptions.domain_exception import HTTP_201_CREATED
from src.shared.infrastructure.api.api_response import success_response
from src.shared.infrastructure.api.views.commad_api_view import CommandAPIView


class CreateAPIView(CommandAPIView):
  view_name = "CreateAPIView"

  def create(self, request):
    validated_data = self._validate_request_serializer(request.data)

    command = self.application_command(validated_data)

    self.infrastructure_command_bus.dispatch(command)

    return success_response(
      message=self.message_response if self.message_response is not None else "Recurso creado exitosamente.",
      status_code=HTTP_201_CREATED,
    )
