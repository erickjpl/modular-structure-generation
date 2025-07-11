from typing import Any

from src.orders.application.subscribers.log_order_created_subscriber import LogOrderCreatedSubscriber
from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_handler import CommandHandler
from src.shared.infrastructure.api.exceptions.internal_server_error_exception import InternalServerErrorException
from src.shared.infrastructure.api.views.base_api_view import BaseAPIView
from src.shared.infrastructure.command_bus.command_handlers import CommandHandlers
from src.shared.infrastructure.command_bus.in_memory_command_bus import InMemoryCommandBus
from src.shared.infrastructure.event_bus.domain_event_subscribers import DomainEventSubscribers
from src.shared.infrastructure.event_bus.in_memory_async_event_bus import InMemoryAsyncEventBus


class DIContainer:
  def __init__(self):
    self._services: dict[str, Any] = {}
    self._tagged_services: dict[str, dict[str, Any]] = {"domainEventSubscriber": {}}

  def register_service(self, key: str, service: Any, tags: list[str] = None):
    if tags is None:
      tags = []

    self._services[key] = service
    for tag in tags:
      if tag not in self._tagged_services:
        self._tagged_services[tag] = {}
      self._tagged_services[tag][key] = "definition_placeholder"

  def get(self, key: str) -> Any:
    return self._services.get(key)

  def find_tagged_service_ids(self, tag: str) -> dict[str, Any]:
    return self._tagged_services.get(tag, {})


class CommandAPIView(BaseAPIView):
  application_command = Command
  application_command_handler = CommandHandler
  application_service = None
  infrastructure_command_bus = InMemoryCommandBus
  infrastructure_event_bus = InMemoryAsyncEventBus
  infrastructure_command_handlers = CommandHandlers
  _initialized = False

  def __init__(self, **kwargs):
    print(f"CommandAPIView __init__ {self.__class__.__name__}")
    super().__init__(**kwargs)
    if not self._initialized:
      self._initialize_components()
      self._initialized = True

  def dispatch(self, request, *args, **kwargs):
    print(f"CommandAPIView dispatch {self.__class__.__name__}")
    try:
      return super().dispatch(request, *args, **kwargs)
    except Exception as exc:
      return self.handle_exception(exc)

  def _initialize_components(self):
    try:
      self._validate_required_attributes()
      self._initialize_repositories()
      self._initialize_event_bus()
      self._initialize_command_bus()
    except Exception as exc:
      return self.handle_exception(exc)

  def _validate_required_attributes(self):
    required_attrs = {
      "repositories": "repositories",
      "application_service": "application_service",
      "request_serializer_class": "request_serializer_class",
      "application_command": "application_command",
      "application_command_handler": "application_command_handler",
    }

    for attr, var_name in required_attrs.items():
      if not getattr(self, attr, None):
        raise InternalServerErrorException(detail=self.__message_detail__(var_name))

    if not issubclass(self.application_command, Command):
      raise InternalServerErrorException(detail=self.__message_detail__("application_command"))
    if not issubclass(self.application_command_handler, CommandHandler):
      raise InternalServerErrorException(detail=self.__message_detail__("application_command_handler"))

  def _initialize_repositories(self):
    self.instantiated_repositories = {}
    for repo_name, repo_class in self.repositories:
      self.instantiated_repositories[repo_name] = repo_class()

  def _initialize_event_bus(self):
    container = DIContainer()
    log_subscriber = LogOrderCreatedSubscriber()
    container.register_service("logProductCreatedSubscriber", log_subscriber, tags=["domainEventSubscriber"])
    all_subscribers = DomainEventSubscribers.from_container(container)

    self.event_bus = self.infrastructure_event_bus()
    self.event_bus.add_subscribers(all_subscribers)

  def _initialize_command_bus(self):
    service = self.application_service(self.event_bus, **self.instantiated_repositories)
    command_handler = self.application_command_handler(service=service)
    command_handlers = self.infrastructure_command_handlers(command_handlers=[command_handler])
    self.infrastructure_command_bus = self.infrastructure_command_bus(command_handlers_information=command_handlers)

  def __message_detail__(self, variable: str):
    return f"{variable} must be defined for this {self.view_name}."
