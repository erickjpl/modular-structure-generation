from enum import Enum, auto
from typing import Protocol, runtime_checkable

from core.generator.base_generator import BaseGenerator


class LanguageOption(Enum):
  PYTHON = "python"


class FrameworkOption(Enum): ...


@runtime_checkable
class LanguagePlugin(Protocol):
  @property
  def language_name(self) -> LanguageOption: ...

  @property
  def supported_frameworks(self) -> list[FrameworkOption]: ...

  def get_generator(self, framework: FrameworkOption | None = None) -> BaseGenerator: ...


# ==============================
# Domain Models (Enums y Clases Base)
# ==============================
class LayerType(Enum):
  DOMAIN = auto()
  APPLICATION = auto()
  INFRASTRUCTURE = auto()


class DomainOption(Enum):
  ENTITIES = "entities"
  VALUE_OBJECTS = "value_objects"
  SERVICES = "services"
  REPOSITORIES = "repositories"
  EVENTS = "events"


# ==============================
# Application Models (Enums y Clases Base)
# ==============================
class ApplicationOption(Enum):
  COMMANDS = "commands"
  QUERIES = "queries"
  HANDLERS = "handlers"
  SERVICES = "services"
  DTOS = "dtos"


class CommandOption(Enum):
  CREATE = "create"
  UPDATE = "update"
  DELETE = "delete"


class QueryOption(Enum):
  LIST = "list"
  READ = "read"


# ==============================
# Infrastructure Models (Enums y Clases Base)
# ==============================
class InfrastructureOption(Enum):
  PERSISTENCE = "persistence"
  API = "api"
  CONSUMERS = "consumers"
  EVENTS = "events"


class PersistenceOption(Enum):
  ENTITY_MODEL = "entity_model"
  ENTITY_REPOSITORY = "entity_repository"


class ApiOption(Enum):
  ROUTES = "urls"
  VIEWS = "views"
  SERIALIZERS = "serializers"


class ViewOption(Enum):
  LIST_VIEW = "list_view"
  CREATE_VIEW = "create_view"
  READ_VIEW = "read_view"
  UPDATE_VIEW = "update_view"
  DELETE_VIEW = "delete_view"


class SerializerOption(Enum):
  LIST_SERIALIZER = "list_serializer"
  READ_SERIALIZER = "read_serializer"
