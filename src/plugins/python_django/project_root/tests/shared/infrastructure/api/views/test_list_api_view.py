from unittest.mock import MagicMock, patch

import pytest
from django.forms import ValidationError
from rest_framework.status import HTTP_200_OK

from src.shared.infrastructure.api.views.base_api_view import BaseAPIView
from src.shared.infrastructure.api.views.list_api_view import ListAPIView
from src.shared.infrastructure.query_bus.in_memory_query_bus import InMemoryQueryBus


class MockRepo:
  pass


class MockQuery:
  def __init__(self, skip: int = 0, limit: int = 50):
    self.skip = skip
    self.limit = limit

  def __eq__(self, other):
    return isinstance(other, MockQuery) and self.skip == other.skip and self.limit == other.limit


class MockQueryHandler:
  def __init__(self, *args, **kwargs):
    pass

  def subscribed_to(self):
    return MockQuery


class MockSerializer:
  def __init__(self, data=None, many=False):
    self._data = data
    self._many = many
    self.errors = {"field": ["error"]}

  def is_valid(self, raise_exception=False):
    return True

  @property
  def data(self):
    return self._data


class TestListAPIView:
  @pytest.fixture
  def view(self):
    class TestableListAPIView(ListAPIView):
      repositories = [("mock_repo", MockRepo)]
      application_query = MockQuery
      application_query_handler = MockQueryHandler
      response_serializer_class = MagicMock(spec=MockSerializer)
      _initialized = False

    test_view = TestableListAPIView()

    test_view.infrastructure_query_bus = MagicMock(spec=InMemoryQueryBus)
    return test_view

  def test_list_success_with_default_pagination(self, view):
    request = MagicMock(query_params={})
    mock_items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
    view.infrastructure_query_bus.ask.return_value = mock_items
    view.response_serializer_class.return_value.data = mock_items

    response = view.list(request)

    view.infrastructure_query_bus.ask.assert_called_once_with(MockQuery(skip=0, limit=50))
    assert response.status_code == HTTP_200_OK
    assert response.data["message"] == "Recursos obtenidos exitosamente."
    assert response.data["data"] == mock_items

  def test_list_success_with_custom_pagination(self, view):
    request = MagicMock(query_params={"skip": "10", "limit": "20"})
    mock_items = [{"id": 3, "name": "Item 3"}]
    view.infrastructure_query_bus.ask.return_value = mock_items
    view.response_serializer_class.return_value.data = mock_items

    response = view.list(request)

    view.infrastructure_query_bus.ask.assert_called_once_with(MockQuery(skip=10, limit=20))
    assert response.status_code == HTTP_200_OK
    assert response.data["data"] == mock_items

  def test_list_success_with_custom_message(self, view):
    request = MagicMock(query_params={})
    view.message_response = "My custom list message"
    mock_items = []
    view.infrastructure_query_bus.ask.return_value = mock_items
    view.response_serializer_class.return_value.data = mock_items

    response = view.list(request)

    assert response.status_code == HTTP_200_OK
    assert response.data["message"] == "My custom list message"

  def test_list_returns_empty_data_when_no_items(self, view):
    request = MagicMock(query_params={})
    view.infrastructure_query_bus.ask.return_value = []
    view.response_serializer_class.return_value.data = []

    response = view.list(request)

    assert response.status_code == HTTP_200_OK
    assert response.data["data"] == []

  def test_list_raises_validation_error_on_serialization_failure(self, view):
    request = MagicMock(query_params={})
    view.infrastructure_query_bus.ask.return_value = [{"id": 1}]

    mock_serializer_instance = MagicMock()
    mock_serializer_instance.is_valid.return_value = False
    mock_serializer_instance.errors = {"detail": "Invalid data"}
    view.response_serializer_class.return_value = mock_serializer_instance

    with pytest.raises(ValidationError) as excinfo:
      view.list(request)

    assert "Invalid data" in str(excinfo.value)

  @patch.object(ListAPIView, "handle_exception")
  @patch.object(BaseAPIView, "dispatch")
  def test_list_handles_generic_exception(self, mock_base_dispatch, mock_handle_exception, view):
    request = MagicMock(query_params={})
    error = Exception("Something went wrong")
    mock_base_dispatch.side_effect = error

    view.dispatch(request)

    mock_handle_exception.assert_called_once_with(error)
