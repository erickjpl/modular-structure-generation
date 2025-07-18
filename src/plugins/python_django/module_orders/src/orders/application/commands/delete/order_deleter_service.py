from src.orders.domain.order_repository import IOrderRepository
from src.orders.domain.value_objects.order_id import OrderId
from src.shared.domain.events.event_bus import EventBus


class OrderDeleterService:
  def __init__(self, repository: IOrderRepository, event_bus: EventBus):
    self.repository = repository
    self.event_bus = event_bus

  def run(self, order_id: OrderId):
    order = self.repository.get_by_id(order_id)
    if order:
      self.repository.delete(order_id)
      self.event_bus.publish(order.pull_domain_events())
