from unittest.mock import MagicMock, patch

import pytest
from django.forms import ValidationError
from rest_framework.status import HTTP_200_OK

from src.shared.infrastructure.api.api_response import success_response
from src.shared.infrastructure.api.views.retrieve_api_view import RetrieveAPIView
from src.shared.infrastructure.query_bus.in_memory_query_bus import InMemoryQueryBus
from src.shared.infrastructure.api.views.base_api_view import BaseAPIView


# --- Mocks and Dummies ---
class MockRepo:
    pass

class MockQuery:
    def __init__(self, pk: str):
        self.pk = pk

    def __eq__(self, other):
        return isinstance(other, MockQuery) and self.pk == other.pk

class MockQueryHandler:
    def __init__(self, *args, **kwargs):
        pass

    def subscribed_to(self):
        return MockQuery

class MockSerializer:
    def __init__(self, instance=None, data=None):
        self._instance = instance
        self._data = data
        self.errors = {"field": ["error"]}

    def is_valid(self, raise_exception=False):
        return True

    @property
    def data(self):
        return self._instance if self._instance is not None else self._data


# --- Test Class ---
class TestRetrieveAPIView:

    @pytest.fixture
    def view(self):
        class TestableRetrieveAPIView(RetrieveAPIView):
            repositories = [("mock_repo", MockRepo)]
            application_query = MockQuery
            application_query_handler = MockQueryHandler
            response_serializer_class = MagicMock(spec=MockSerializer) # Mock the class itself
            _initialized = False # Ensure re-initialization for each test

        test_view = TestableRetrieveAPIView()
        # Mock the query bus for direct control over its behavior
        test_view.infrastructure_query_bus = MagicMock(spec=InMemoryQueryBus)
        return test_view

    def test_retrieve_success(self, view):
        # Arrange
        pk = "test-id"
        request = MagicMock()
        mock_item = {"id": pk, "name": "Test Item"}
        view.infrastructure_query_bus.ask.return_value = mock_item
        view.response_serializer_class.return_value.data = mock_item # Set data on the mock instance

        # Act
        response = view.get(request, pk)

        # Assert
        view.infrastructure_query_bus.ask.assert_called_once_with(MockQuery(pk=pk))
        assert response.status_code == HTTP_200_OK
        assert response.data["message"] == f"Recurso {pk} obtenido exitosamente."
        assert response.data["data"] == mock_item

    def test_retrieve_not_found(self, view):
        # Arrange
        pk = "not-found-id"
        request = MagicMock()
        view.infrastructure_query_bus.ask.return_value = None # Simulate item not found

        # Act
        response = view.get(request, pk)

        # Assert
        assert response.status_code == HTTP_200_OK # Or whatever status code is expected for not found
        assert response.data["data"] is None # Or an empty dict/list depending on expected behavior

    def test_retrieve_with_custom_message(self, view):
        # Arrange
        pk = "test-id"
        request = MagicMock()
        mock_item = {"id": pk, "name": "Test Item"}
        view.infrastructure_query_bus.ask.return_value = mock_item
        view.response_serializer_class.return_value.data = mock_item
        view.message_response = "My custom retrieve message"

        # Act
        response = view.get(request, pk)

        # Assert
        assert response.status_code == HTTP_200_OK
        assert response.data["message"] == "My custom retrieve message"

    def test_retrieve_raises_validation_error_on_serialization_failure(self, view):
        # Arrange
        pk = "test-id"
        request = MagicMock()
        mock_item = {"id": pk, "name": "Test Item"}
        view.infrastructure_query_bus.ask.return_value = mock_item
        # Mock serializer to fail validation
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {"detail": "Invalid data"}
        view.response_serializer_class.return_value = mock_serializer_instance

        # Act & Assert
        with pytest.raises(ValidationError) as excinfo:
            view.get(request, pk)

        assert "Invalid data" in str(excinfo.value)

    @patch.object(RetrieveAPIView, 'handle_exception')
    @patch.object(BaseAPIView, 'dispatch') # Patch BaseAPIView's dispatch
    def test_retrieve_handles_generic_exception(self, mock_base_dispatch, mock_handle_exception, view):
        # Arrange
        pk = "test-id"
        request = MagicMock()
        error = Exception("Something went wrong")
        mock_base_dispatch.side_effect = error # Make BaseAPIView.dispatch raise the error

        # Act
        view.dispatch(request, pk=pk)

        # Assert
        mock_handle_exception.assert_called_once_with(error)
