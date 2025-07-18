from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from src.shared.domain.commands.command import Command
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.seller_name import SellerName
from src.orders.domain.entities.order import OrderSource, OrderStatus


@dataclass(frozen=True)
class UpdateOrderCommand(Command):
  order_id: OrderId
  order_number: Optional[OrderNumber] = None
  customer_name: Optional[CustomerName] = None
  seller_name: Optional[SellerName] = None
  ip_address: Optional[str] = None
  source: Optional[OrderSource] = None
  status: Optional[OrderStatus] = None
  currency: Optional[str] = None
  total_amount: Optional[Decimal] = None
