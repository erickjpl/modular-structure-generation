from src.orders.application.dtos.order_dto import OrderDTO
from src.orders.application.queries.list.order_list_query import OrderListQuery
from src.orders.domain.order_repository import IOrderRepository
from src.shared.domain.queries.query_handler import QueryHandler


class OrderListQueryHandler(QueryHandler[OrderListQuery, OrderDTO]):
  def __init__(self, repository: IOrderRepository):
    self._repository = repository

  def subscribed_to(self) -> type[OrderListQuery]:
    return OrderListQuery

  def handle(self, query: OrderListQuery) -> list[OrderDTO]:
    orders = self._repository.get_all(skip=query.skip, limit=query.limit)

    return [OrderDTO.from_entity(order) for order in orders]
