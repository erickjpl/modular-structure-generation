from typing import TypeVar

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.query_handler import QueryHandler
from src.shared.domain.queries.query_not_registered_error import QueryNotRegisteredError
from src.shared.domain.queries.response import Response

R = TypeVar("R", bound=Response)
Q = TypeVar("Q", bound=Query)


class QueryHandlers:
  def __init__(self, query_handlers: list[QueryHandler[Q, R]]):
    self.__handlers: dict[type[Query], QueryHandler[Q, R]] = {}

    for handler in query_handlers:
      self.__handlers[handler.subscribed_to()] = handler

  def get(self, query: Query) -> QueryHandler[Q, R]:
    query_handler = self.__handlers.get(query.__class__)

    if not query_handler:
      raise QueryNotRegisteredError(query)

    return query_handler
