from unittest.mock import MagicMock, patch

import pytest

from src.shared.infrastructure.api.exceptions.internal_server_error_exception import InternalServerErrorException
from src.shared.infrastructure.api.views.query_api_view import QueryAPIView


class MockRepo:
  pass


class FaultyRepo:
  def __init__(self):
    raise ValueError("Repo connection failed")


class MockQuery:
  pass


class MockQueryHandler:
  def __init__(self, *args, **kwargs):
    pass

  def subscribed_to(self):
    return MockQuery


class MockSerializer:
  pass


class TestQueryAPIView:
  @pytest.fixture
  def valid_view_class(self):
    class ValidQueryView(QueryAPIView):
      repositories = [("mock_repo", MockRepo)]
      application_query = MockQuery
      application_query_handler = MockQueryHandler
      response_serializer_class = MockSerializer
      _initialized = False

    return ValidQueryView

  @patch.object(QueryAPIView, "handle_exception")
  def test_initialization_fails_if_repositories_is_missing(self, mock_handle_exception):
    class InvalidView(QueryAPIView):
      application_query = MockQuery
      application_query_handler = MockQueryHandler
      response_serializer_class = MockSerializer
      repositories = None
      _initialized = False

    InvalidView()
    mock_handle_exception.assert_called_once()
    exception = mock_handle_exception.call_args[0][0]
    assert isinstance(exception, InternalServerErrorException)
    assert "repositories debe ser definido" in str(exception)

  @patch.object(QueryAPIView, "handle_exception")
  def test_initialization_fails_if_application_query_is_missing(self, mock_handle_exception):
    class InvalidView(QueryAPIView):
      repositories = [("mock_repo", MockRepo)]
      application_query_handler = MockQueryHandler
      response_serializer_class = MockSerializer
      application_query = None
      _initialized = False

    InvalidView()
    mock_handle_exception.assert_called_once()
    exception = mock_handle_exception.call_args[0][0]
    assert isinstance(exception, InternalServerErrorException)
    assert "application_query debe ser definido" in str(exception)

  @patch.object(QueryAPIView, "handle_exception")
  def test_initialization_fails_if_query_handler_is_missing(self, mock_handle_exception):
    class InvalidView(QueryAPIView):
      repositories = [("mock_repo", MockRepo)]
      application_query = MockQuery
      response_serializer_class = MockSerializer
      application_query_handler = None
      _initialized = False

    InvalidView()
    mock_handle_exception.assert_called_once()
    exception = mock_handle_exception.call_args[0][0]
    assert isinstance(exception, InternalServerErrorException)
    assert "application_query_handler debe ser definido" in str(exception)

  @patch.object(QueryAPIView, "handle_exception")
  def test_initialization_fails_if_serializer_is_missing(self, mock_handle_exception):
    class InvalidView(QueryAPIView):
      repositories = [("mock_repo", MockRepo)]
      application_query = MockQuery
      application_query_handler = MockQueryHandler
      response_serializer_class = None
      _initialized = False

    InvalidView()
    mock_handle_exception.assert_called_once()
    exception = mock_handle_exception.call_args[0][0]
    assert isinstance(exception, InternalServerErrorException)
    assert "response_serializer_class debe ser definido" in str(exception)

  def test_successful_initialization(self, valid_view_class):
    view = valid_view_class()

    assert hasattr(view, "instantiated_repositories")
    assert "mock_repo" in view.instantiated_repositories
    assert isinstance(view.instantiated_repositories["mock_repo"], MockRepo)
    assert hasattr(view, "infrastructure_query_bus")

  @patch("src.shared.infrastructure.api.views.base_api_view.BaseAPIView.dispatch")
  def test_dispatch_handles_exception(self, mock_super_dispatch, valid_view_class):
    view = valid_view_class()
    view.handle_exception = MagicMock()
    error = Exception("Dispatch Error")
    mock_super_dispatch.side_effect = error
    request = MagicMock()

    view.dispatch(request)

    view.handle_exception.assert_called_once_with(error)

  def test_initialization_with_empty_repositories_list(self, valid_view_class):
    valid_view_class.repositories = []

    view = valid_view_class()

    assert view.instantiated_repositories == {}
    assert hasattr(view, "infrastructure_query_bus")

  @patch.object(QueryAPIView, "handle_exception")
  def test_initialization_handles_faulty_repository(self, mock_handle_exception, valid_view_class):
    valid_view_class.repositories = [("faulty_repo", FaultyRepo)]

    valid_view_class()

    mock_handle_exception.assert_called_once()
    exception = mock_handle_exception.call_args[0][0]
    assert isinstance(exception, ValueError)
    assert "Repo connection failed" in str(exception)

  def test_initialization_is_only_run_once_per_class(self, valid_view_class):
    with patch.object(valid_view_class, "_initialize_components") as mock_init:
      view1 = valid_view_class()
      assert mock_init.call_count == 1

      view2 = valid_view_class()
      assert mock_init.call_count == 1
