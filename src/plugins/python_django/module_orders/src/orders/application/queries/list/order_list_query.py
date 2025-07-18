from dataclasses import dataclass

from src.shared.domain.queries.query import Query


@dataclass(frozen=True)
class OrderListQuery(Query):
  skip: int = 0
  limit: int = 100
