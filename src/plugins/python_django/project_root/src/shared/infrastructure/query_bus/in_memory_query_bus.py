from typing import TypeVar

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.query_bus import QueryBus
from src.shared.domain.queries.query_not_registered_error import QueryNotRegisteredError
from src.shared.domain.queries.response import Response
from src.shared.infrastructure.query_bus.query_handlers import QueryHandlers

R_co = TypeVar("R_co", bound=Response, covariant=True)


class InMemoryQueryBus(QueryBus):
  def __init__(self, query_handlers_information: QueryHandlers):
    self.__query_handlers_information = query_handlers_information

  def ask(self, query: Query) -> R_co:
    handler = self.__query_handlers_information.get(query)

    if not handler:
      raise QueryNotRegisteredError(query)

    return handler.handle(query)