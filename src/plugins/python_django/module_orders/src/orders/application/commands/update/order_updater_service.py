from decimal import Decimal
from typing import Optional

from src.orders.domain.entities.order import OrderStatus, OrderSource
from src.orders.domain.order_repository import IOrderRepository
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.seller_name import SellerName
from src.orders.domain.value_objects.total_amount import TotalAmount
from src.shared.domain.events.event_bus import EventBus


class OrderUpdaterService:
  def __init__(self, repository: IOrderRepository, event_bus: EventBus):
    self.repository = repository
    self.event_bus = event_bus

  def run(
    self,
    order_id: OrderId,
    order_number: Optional[OrderNumber] = None,
    customer_name: Optional[CustomerName] = None,
    seller_name: Optional[SellerName] = None,
    ip_address: Optional[str] = None,
    source: Optional[OrderSource] = None,
    status: Optional[OrderStatus] = None,
    currency: Optional[str] = None,
    total_amount: Optional[Decimal] = None,
  ):
    order = self.repository.get_by_id(order_id)

    if order:
      if order_number:
        order._order_number = order_number
      if customer_name:
        order._customer_name = customer_name
      if seller_name:
        order._seller_name = seller_name
      if ip_address:
        order._ip_address = ip_address
      if source:
        order._source = source
      if status:
        order.update_status(status)
      if currency:
        order._currency = currency
      

      self.repository.save(order)
      self.event_bus.publish(order.pull_domain_events())
