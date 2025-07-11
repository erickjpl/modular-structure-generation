from unittest.mock import MagicMock

import pytest
from rest_framework.status import HTTP_204_NO_CONTENT

from src.shared.domain.commands.command_bus import CommandBus
from src.shared.infrastructure.api.views.delete_api_view import DestroyAPIView


class DummyCommand:
  def __init__(self, *args, **kwargs):
    pass


@pytest.fixture
def command_bus():
  return MagicMock(spec=CommandBus)


@pytest.fixture
def view(command_bus):
  view = DestroyAPIView()
  view.infrastructure_command_bus = command_bus
  view.application_command = DummyCommand
  view.message_response = None
  return view


class TestDestroyAPIView:
  def test_destroy_success_and_dispatches_command(self, view):
    pk = "some-id"
    request = MagicMock()

    response = view.destroy(request, pk)

    assert response.status_code == HTTP_204_NO_CONTENT
    view.infrastructure_command_bus.dispatch.assert_called_once()

  def test_destroy_returns_default_message(self, view):
    pk = "some-id"
    request = MagicMock()

    response = view.destroy(request, pk)

    assert response.data["message"] == f"Recurso {pk} eliminado exitosamente."

  def test_destroy_returns_custom_message_when_provided(self, view):
    pk = "some-id"
    request = MagicMock()
    custom_message = "Custom delete message"
    view.message_response = custom_message

    response = view.destroy(request, pk)

    assert response.status_code == HTTP_204_NO_CONTENT
    assert response.data["message"] == custom_message
    view.infrastructure_command_bus.dispatch.assert_called_once()

  def test_destroy_handles_exceptions_from_command_bus(self, view):
    pk = "some-id"
    request = MagicMock()
    error_message = "Command bus failed"
    view.infrastructure_command_bus.dispatch.side_effect = Exception(error_message)

    with pytest.raises(Exception) as excinfo:
      view.destroy(request, pk)

    assert str(excinfo.value) == error_message
