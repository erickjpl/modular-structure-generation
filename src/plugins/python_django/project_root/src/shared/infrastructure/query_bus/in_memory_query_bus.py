from typing import TypeVar

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.query_bus import QueryBus
from src.shared.domain.queries.response import Response
from src.shared.infrastructure.query_bus.query_handlers import QueryHandlers

R_co = TypeVar("R_co", bound=Response, covariant=True)


class InMemoryQueryBus(QueryBus):
  def __init__(self, query_handlers_information: QueryHandlers):
    self.__query_handlers_information = query_handlers_information

  async def ask(self, query: Query) -> R_co:
    handler = self.__query_handlers_information.get(query)
    return await handler.handle(query)
