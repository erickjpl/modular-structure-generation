from unittest.mock import Mock, patch

import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from src.shared.domain.commands.command import Command
from src.shared.domain.exceptions.domain_exception import (
  HTTP_201_CREATED,
  HTTP_400_BAD_REQUEST,
  HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.shared.infrastructure.api.views.create_api_view import CreateAPIView


class DummyCommand(Command):
  def __init__(self, data):
    self.data = data


class DummyCreateAPIView(CreateAPIView):
  request_serializer_class = Mock

  def application_command(self, validated_data):
    return DummyCommand(validated_data)


@pytest.mark.django_db
@patch("src.shared.infrastructure.api.views.commad_api_view.CommandAPIView.infrastructure_command_bus")
class TestCreateAPIView:
  def setup_method(self):
    self.factory = APIRequestFactory()
    self.request_data = {"test": "data"}
    self.view = DummyCreateAPIView.as_view({"post": "create"})

  def test_create_success(self, mock_command_bus):
    request = self.factory.post("/fake-url/", self.request_data, format="json")
    mock_command_bus.dispatch = Mock()
    with patch.object(DummyCreateAPIView, "_validate_request_serializer", return_value=self.request_data):
      response = self.view(request)

    mock_command_bus.dispatch.assert_called_once()
    dispatched_command = mock_command_bus.dispatch.call_args[0][0]
    assert isinstance(dispatched_command, DummyCommand)
    assert dispatched_command.data == self.request_data
    assert response.status_code == HTTP_201_CREATED
    assert response.data["message"] == "Recurso creado exitosamente."

  def test_create_success_with_custom_message(self, mock_command_bus):
    class CustomMessageView(DummyCreateAPIView):
      message_response = "Custom success message."

    view = CustomMessageView.as_view({"post": "create"})
    request = self.factory.post("/fake-url/", self.request_data, format="json")
    mock_command_bus.dispatch = Mock()
    with patch.object(CustomMessageView, "_validate_request_serializer", return_value=self.request_data):
      response = view(request)

    assert response.status_code == HTTP_201_CREATED
    assert response.data["message"] == "Custom success message."

  def test_create_raises_validation_error(self, mock_command_bus):
    request = self.factory.post("/fake-url/", {}, format="json")
    error_detail = {"field": ["error message"]}

    with patch.object(DummyCreateAPIView, "_validate_request_serializer", side_effect=ValidationError(error_detail)):
      response = self.view(request)

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.data["error"]["extra"] == error_detail
    mock_command_bus.dispatch.assert_not_called()

  def test_create_handles_command_bus_exception(self, mock_command_bus):
    request = self.factory.post("/fake-url/", self.request_data, format="json")
    mock_command_bus.dispatch.side_effect = Exception("Bus error")
    with patch.object(DummyCreateAPIView, "_validate_request_serializer", return_value=self.request_data):
      response = self.view(request)

    assert response.status_code == HTTP_500_INTERNAL_SERVER_ERROR
    mock_command_bus.dispatch.assert_called_once()
