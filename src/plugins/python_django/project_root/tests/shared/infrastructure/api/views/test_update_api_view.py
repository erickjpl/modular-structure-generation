from unittest.mock import MagicMock, patch

import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_200_OK

from src.shared.domain.commands.command_bus import CommandBus
from src.shared.infrastructure.api.exceptions.not_found_exception import NotFoundException
from src.shared.infrastructure.api.views.update_api_view import UpdateAPIView


class DummyCommand:
    def __init__(self, *args, **kwargs):
        pass


@pytest.fixture
def command_bus():
    return MagicMock(spec=CommandBus)


@pytest.fixture
def view(command_bus):
    view = UpdateAPIView()
    view.infrastructure_command_bus = command_bus
    view.application_command = DummyCommand
    view.message_response = None
    view._validate_request_serializer = MagicMock(side_effect=lambda data, **kwargs: data)
    return view


class TestUpdateAPIView:
    # --- PUT / UPDATE Method Tests ---
    def test_update_success(self, view):
        pk = "test-id"
        request_data = {"key": "value"}
        request = MagicMock(data=request_data)
        view.infrastructure_command_bus.dispatch.return_value = {"id": pk}

        response = view.update(request, pk)

        assert response.status_code == HTTP_200_OK
        assert response.data["message"] == f"Recurso {pk} actualizado exitosamente."
        view.infrastructure_command_bus.dispatch.assert_called_once()

    def test_update_raises_not_found(self, view):
        pk = "not-found-id"
        request_data = {"key": "value"}
        request = MagicMock(data=request_data)
        view.infrastructure_command_bus.dispatch.return_value = None

        with pytest.raises(NotFoundException) as excinfo:
            view.update(request, pk)

        assert str(excinfo.value) == f"Recurso con ID {pk} no encontrado para actualización."

    def test_update_with_custom_message(self, view):
        pk = "test-id"
        request_data = {"key": "value"}
        request = MagicMock(data=request_data)
        custom_message = "Item updated!"
        view.message_response = custom_message
        view.infrastructure_command_bus.dispatch.return_value = {"id": pk}

        response = view.update(request, pk)

        assert response.status_code == HTTP_200_OK
        assert response.data["message"] == custom_message

    def test_update_handles_command_bus_exception(self, view):
        pk = "test-id"
        request = MagicMock(data={"key": "value"})
        view.infrastructure_command_bus.dispatch.side_effect = Exception("Bus Error")

        with pytest.raises(Exception) as excinfo:
            view.update(request, pk)

        assert str(excinfo.value) == "Bus Error"

    def test_update_handles_validation_error(self, view):
        pk = "test-id"
        request = MagicMock(data={"key": "invalid"})
        view._validate_request_serializer.side_effect = ValidationError("Invalid data")

        with pytest.raises(ValidationError) as excinfo:
            view.update(request, pk)

        assert "Invalid data" in str(excinfo.value)

    # --- PATCH Method Tests ---
    def test_patch_success(self, view):
        pk = "test-id"
        request_data = {"key": "new_value"}
        request = MagicMock(data=request_data)
        view.infrastructure_command_bus.dispatch.return_value = {"id": pk}

        response = view.patch(request, pk)

        assert response.status_code == HTTP_200_OK
        assert response.data["message"] == f"Recurso {pk} actualizado parcialmente exitosamente."
        view.infrastructure_command_bus.dispatch.assert_called_once()
        view._validate_request_serializer.assert_called_with(request_data, partial=True)

    def test_patch_raises_not_found(self, view):
        pk = "not-found-id"
        request_data = {"key": "value"}
        request = MagicMock(data=request_data)
        view.infrastructure_command_bus.dispatch.return_value = None

        with pytest.raises(NotFoundException) as excinfo:
            view.patch(request, pk)

        assert str(excinfo.value) == f"Recurso con ID {pk} no encontrado para actualización parcial."

    def test_patch_with_custom_message(self, view):
        pk = "test-id"
        request_data = {"key": "value"}
        request = MagicMock(data=request_data)
        custom_message = "Item partially updated!"
        view.message_response = custom_message
        view.infrastructure_command_bus.dispatch.return_value = {"id": pk}

        response = view.patch(request, pk)

        assert response.status_code == HTTP_200_OK
        assert response.data["message"] == custom_message

    def test_patch_handles_command_bus_exception(self, view):
        pk = "test-id"
        request = MagicMock(data={"key": "value"})
        view.infrastructure_command_bus.dispatch.side_effect = Exception("Bus Error")

        with pytest.raises(Exception) as excinfo:
            view.patch(request, pk)

        assert str(excinfo.value) == "Bus Error"

    def test_patch_handles_validation_error(self, view):
        pk = "test-id"
        request = MagicMock(data={"key": "invalid"})
        view._validate_request_serializer.side_effect = ValidationError("Invalid partial data")

        with pytest.raises(ValidationError) as excinfo:
            view.patch(request, pk)

        assert "Invalid partial data" in str(excinfo.value)