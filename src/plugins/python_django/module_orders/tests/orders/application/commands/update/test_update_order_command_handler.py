import uuid
from decimal import Decimal
from unittest.mock import Mock

import pytest

from src.orders.application.commands.update.order_updater_service import OrderUpdaterService
from src.orders.application.commands.update.update_order_command import UpdateOrderCommand
from src.orders.application.commands.update.update_order_command_handler import UpdateOrderCommandHandler
from src.orders.domain.entities.order import OrderSource, OrderStatus
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.seller_name import SellerName


@pytest.fixture
def mock_order_updater_service():
  return Mock(spec=OrderUpdaterService)


def test_update_order_command_handler_subscribed_to():
  handler = UpdateOrderCommandHandler(service=Mock())
  assert handler.subscribed_to() == UpdateOrderCommand


def test_update_order_command_handler_handle(mock_order_updater_service):
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

  handler = UpdateOrderCommandHandler(service=mock_order_updater_service)

  handler.handle(command)

  mock_order_updater_service.run.assert_called_once_with(
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
