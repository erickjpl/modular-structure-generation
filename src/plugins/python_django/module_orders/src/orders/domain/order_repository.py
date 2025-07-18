from abc import ABC, abstractmethod

from src.orders.domain.entities.order import Order
from src.orders.domain.value_objects.order_id import OrderId


class IOrderRepository(ABC):
  @abstractmethod
  def get_all(self) -> list[Order]:
    pass

  @abstractmethod
  def get_by_id(self, order_id: OrderId) -> Order | None:
    pass

  @abstractmethod
  def save(self, order: Order):
    pass

  @abstractmethod
  def delete(self, order_id: OrderId):
    pass
