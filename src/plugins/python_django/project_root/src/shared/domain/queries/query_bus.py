from abc import ABC, abstractmethod
from typing import TypeVar

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.response import Response

R = TypeVar("R", bound=Response)
QueryType = TypeVar("QueryType", bound=Query)


class QueryBus[R: Response](ABC):
  @abstractmethod
  async def ask(self, query: QueryType) -> R:
    raise NotImplementedError
