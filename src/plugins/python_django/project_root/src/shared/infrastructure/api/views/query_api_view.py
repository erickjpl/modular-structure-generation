from src.shared.domain.queries.query import Query
from src.shared.domain.queries.query_handler import QueryHandler
from src.shared.infrastructure.api.exceptions.internal_server_error_exception import InternalServerErrorException
from src.shared.infrastructure.api.views.base_api_view import BaseAPIView
from src.shared.infrastructure.query_bus.in_memory_query_bus import InMemoryQueryBus
from src.shared.infrastructure.query_bus.query_handlers import QueryHandlers


class QueryAPIView(BaseAPIView):
  application_query = Query
  application_query_handler = QueryHandler
  infrastructure_query_bus = InMemoryQueryBus
  infrastructure_query_handlers = QueryHandlers
  _initialized = False

  def __init__(self, **kwargs):
    print(f"QueryAPIView __init__ {self.__class__.__name__}")
    super().__init__(**kwargs)
    if not self._initialized:
      self._initialize_components()
      self.__class__._initialized = True

  def dispatch(self, request, *args, **kwargs):
    print(f"QueryAPIView dispatch {self.__class__.__name__}")
    try:
      return super().dispatch(request, *args, **kwargs)
    except Exception as exc:
      return self.handle_exception(exc)

  def _initialize_components(self):
    try:
      self._validate_required_attributes()
      self._initialize_repositories()
      self._initialize_query_bus()
    except Exception as exc:
      return self.handle_exception(exc)

  def _validate_required_attributes(self):
    required_attrs = {
      "repositories": "repositories debe ser definido para ListAPIView.",
      "application_query": "application_query debe ser definido para ListAPIView.",
      "application_query_handler": "application_query_handler debe ser definido para ListAPIView.",
      "response_serializer_class": "response_serializer_class debe ser definido para ListAPIView.",
    }

    for attr, error_message in required_attrs.items():
      if getattr(self, attr, None) is None:
        raise InternalServerErrorException(detail=error_message)

  def _initialize_repositories(self):
    self.instantiated_repositories = {}
    for repo_name, repo_class in self.repositories:
      self.instantiated_repositories[repo_name] = repo_class()

  def _initialize_query_bus(self):
    query_handler = self.application_query_handler(**self.instantiated_repositories)
    query_handlers = self.infrastructure_query_handlers(query_handlers=[query_handler])
    self.infrastructure_query_bus = self.infrastructure_query_bus(query_handlers_information=query_handlers)
