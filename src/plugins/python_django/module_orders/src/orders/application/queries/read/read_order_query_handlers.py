from src.orders.application.dtos.order_dto import OrderDTO
from src.orders.application.queries.read.read_order_query import ReadOrderQuery
from src.orders.domain.order_repository import IOrderRepository


class ReadOrderQueryHandler:
  def __init__(self, repository: IOrderRepository):
    self._repository = repository

  def subscribed_to(self) -> type[ReadOrderQuery]:
    return ReadOrderQuery

  def handle(self, query: ReadOrderQuery) -> OrderDTO | None:
    order = self._repository.get_by_id(pk=query.pk)

    if order is None:
      return None

    return OrderDTO.from_entity(order)
