import uuid
from decimal import Decimal

from src.orders.application.commands.update.update_order_command import UpdateOrderCommand
from src.orders.domain.entities.order import OrderSource, OrderStatus
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.seller_name import SellerName


def test_update_order_command_creation():
  order_id = OrderId(str(uuid.uuid4()))
  order_number = OrderNumber("ORD-001")
  customer_name = CustomerName("Updated Customer")
  seller_name = SellerName("Updated Seller")
  ip_address = "192.168.1.100"
  source = OrderSource.MOBILE
  status = OrderStatus.SHIPPED
  currency = "EUR"
  total_amount = Decimal("150.00")

  command = UpdateOrderCommand(
    order_id=order_id,
    order_number=order_number,
    customer_name=customer_name,
    seller_name=seller_name,
    ip_address=ip_address,
    source=source,
    status=status,
    currency=currency,
    total_amount=total_amount,
  )

  assert command.order_id == order_id
  assert command.order_number == order_number
  assert command.customer_name == customer_name
  assert command.seller_name == seller_name
  assert command.ip_address == ip_address
  assert command.source == source
  assert command.status == status
  assert command.currency == currency
  assert command.total_amount == total_amount
