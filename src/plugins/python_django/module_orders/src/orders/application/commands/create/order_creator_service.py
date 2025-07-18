from src.orders.domain.entities.order import Order, OrderSource
from src.orders.domain.order_repository import IOrderRepository
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName
from src.orders.domain.entities.order_item import OrderItem
from src.shared.domain.events.event_bus import EventBus


class OrderCreatorService:
  def __init__(self, repository: IOrderRepository, event_bus: EventBus):
    self.repository = repository
    self.event_bus = event_bus

  def run(
    self,
    order_id: OrderId,
    order_number: OrderNumber,
    customer_id: CustomerId,
    customer_name: CustomerName,
    seller_id: SellerId,
    seller_name: SellerName,
    ip_address: str,
    source: OrderSource,
    currency: str,
    items: list[OrderItem],
  ):
    order = Order.create(
      order_id=order_id,
      order_number=order_number,
      customer_id=customer_id,
      customer_name=customer_name,
      seller_id=seller_id,
      seller_name=seller_name,
      ip_address=ip_address,
      source=source,
      currency=currency,
      items=items,
    )
    self.repository.save(order)
    self.event_bus.publish(order.pull_domain_events())
