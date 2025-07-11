from unittest.mock import Mock

import pytest

from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_handler import CommandHandler
from src.shared.infrastructure.api.exceptions.internal_server_error_exception import InternalServerErrorException
from src.shared.infrastructure.api.views.commad_api_view import CommandAPIView


class MockCommand(Command):
  pass


class MockCommandHandler(CommandHandler):
  def handle(self, command: MockCommand) -> None:
    pass

  @classmethod
  def subscribed_to(cls) -> type[Command]:
    return MockCommand


@pytest.fixture
def mock_command_bus():
  return Mock()


@pytest.fixture
def mock_event_bus():
  return Mock()


@pytest.fixture
def mock_repositories():
  return {"mock_repository": Mock()}


@pytest.fixture
def mock_application_service():
  return Mock()


@pytest.fixture
def mock_request_serializer():
  mock = Mock()
  mock.is_valid.return_value = True
  mock.validated_data = {}
  return mock


@pytest.fixture
def command_api_view(
  mock_command_bus,
  mock_event_bus,
  mock_repositories,
  mock_application_service,
  mock_request_serializer,
):
  view = CommandAPIView()
  view.repositories = mock_repositories
  view.application_service = mock_application_service
  view.request_serializer_class = lambda data, partial=False: mock_request_serializer
  view.application_command = MockCommand
  view.application_command_handler = MockCommandHandler
  view.infrastructure_command_bus = mock_command_bus
  view.infrastructure_event_bus = mock_event_bus
  view._initialized = False
  return view


def test_dispatch_success(command_api_view: CommandAPIView):
  command_api_view.dispatch(request=Mock())


def test_initialize_components_success(command_api_view: CommandAPIView):
  command_api_view._initialize_components()


def test_validate_required_attributes_missing_repositories_raises_exception(command_api_view: CommandAPIView):
  command_api_view.repositories = None
  with pytest.raises(InternalServerErrorException):
    command_api_view._validate_required_attributes()


def test_validate_required_attributes_missing_application_service_raises_exception(command_api_view: CommandAPIView):
  command_api_view.application_service = None
  with pytest.raises(InternalServerErrorException):
    command_api_view._validate_required_attributes()


def test_validate_required_attributes_missing_request_serializer_class_raises_exception(
  command_api_view: CommandAPIView,
):
  command_api_view.request_serializer_class = None
  with pytest.raises(InternalServerErrorException):
    command_api_view._validate_required_attributes()


def test_validate_required_attributes_missing_application_command_raises_exception(command_api_view: CommandAPIView):
  command_api_view.application_command = None
  with pytest.raises(InternalServerErrorException):
    command_api_view._validate_required_attributes()


def test_validate_required_attributes_missing_application_command_handler_raises_exception(
  command_api_view: CommandAPIView,
):
  command_api_view.application_command_handler = None
  with pytest.raises(InternalServerErrorException):
    command_api_view._validate_required_attributes()


def test_initialize_repositories(command_api_view: CommandAPIView):
  command_api_view.repositories = [("mock_repo", Mock)]
  command_api_view._initialize_repositories()
  assert "mock_repo" in command_api_view.instantiated_repositories


def test_initialize_event_bus(command_api_view: CommandAPIView):
  command_api_view._initialize_event_bus()
  assert command_api_view.event_bus is not None


def test_initialize_command_bus(command_api_view: CommandAPIView):
  command_api_view.instantiated_repositories = {}
  command_api_view.event_bus = Mock()
  command_api_view._initialize_command_bus()
  assert command_api_view.infrastructure_command_bus is not None
