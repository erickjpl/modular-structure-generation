from abc import ABC, abstractmethod
from typing import TypeVar

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.response import Response

Q = TypeVar("Q", bound=Query)
R = TypeVar("R", bound=Response)


class QueryHandler[Q: Query, R: Response](ABC):
  @abstractmethod
  def subscribed_to(self) -> type[Query]:
    raise NotImplementedError

  @abstractmethod
  async def handle(self, query: Q) -> R:
    raise NotImplementedError
