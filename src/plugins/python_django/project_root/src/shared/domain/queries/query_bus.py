from abc import ABC, abstractmethod
from typing import TypeVar

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.response import Response

R = TypeVar("R", bound=Response)
Q = TypeVar("Q", bound=Query)


class QueryBus[R: Response](ABC):
  @abstractmethod
  def ask(self, query: Q) -> R:
    raise NotImplementedError
