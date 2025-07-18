from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from src.orders.application.dtos.order_dto import OrderDTO
from src.orders.application.queries.list.order_list_query import OrderListQuery
from src.orders.application.queries.list.order_list_query_handlers import OrderListQueryHandler
from src.orders.domain.entities.order import OrderSource, OrderStatus
from src.orders.domain.order_repository import IOrderRepository
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.seller_id import SellerId


# Fixtures for mocking
@pytest.fixture
def mock_order_repository():
  return Mock(spec=IOrderRepository)


@pytest.fixture
def mock_order_item():
  mock_item = Mock()
  mock_item.product_id = "prod123"
  mock_item.product_name = "Test Product"
  mock_item.product_sku = "TP-001"
  mock_item.product_image_url = "http://example.com/img.jpg"
  mock_item.quantity = 2
  mock_item.unit_price = Decimal("10.00")
  mock_item.subtotal = Decimal("20.00")
  mock_item.discount_amount = Decimal("0.00")
  mock_item.tax_amount = Decimal("1.00")
  mock_item.total = Decimal("21.00")
  mock_item.notes = "Item notes"
  return mock_item


@pytest.fixture
def mock_order(mock_order_item):
  mock_order = Mock()
  mock_order.id = Mock(spec=OrderId)
  mock_order.id.value = "order123"
  mock_order.id.__str__ = lambda s: "order123"
  mock_order.order_date = datetime(2023, 1, 15)
  mock_order.order_number = "ORD-001"
  mock_order.customer_id = Mock(spec=CustomerId)
  mock_order.customer_id.value = "cust456"
  mock_order.customer_id.__str__ = lambda s: "cust456"
  mock_order.customer_name = "John Doe"
  mock_order.seller_id = Mock(spec=SellerId)
  mock_order.seller_id.value = "seller789"
  mock_order.seller_id.__str__ = lambda s: "seller789"
  mock_order.seller_name = "Acme Corp"
  mock_order.ip_address = "192.168.1.1"
  mock_order.source = OrderSource.WEB
  mock_order.status = OrderStatus.PAID
  mock_order.total_items = 1
  mock_order.currency = "USD"
  mock_order.amount = Decimal("20.00")
  mock_order.discount = Decimal("0.00")
  mock_order.tax_amount = Decimal("1.00")
  mock_order.total_amount = Decimal("21.00")
  mock_order.paid_amount = Decimal("21.00")
  mock_order.balance_due = Decimal("0.00")
  mock_order.notes = "Order notes"

  # Mock the items property to return a mock object with an all() method
  mock_order.items = Mock()
  mock_order.items.all.return_value = [mock_order_item]

  return mock_order


def test_order_list_query_handler_subscribed_to():
  handler = OrderListQueryHandler(repository=Mock())
  assert handler.subscribed_to() == OrderListQuery


def test_order_list_query_handler_handle(mock_order_repository, mock_order, mock_order_item):
  mock_order_repository.get_all.return_value = [mock_order]
  handler = OrderListQueryHandler(repository=mock_order_repository)
  query = OrderListQuery(skip=0, limit=10)

  result = handler.handle(query)

  mock_order_repository.get_all.assert_called_once_with(skip=0, limit=10)
  assert len(result) == 1
  assert isinstance(result[0], OrderDTO)

  # Assert some properties of the returned DTO
  assert result[0].id == mock_order.id.value
  assert result[0].order_number == mock_order.order_number
  assert result[0].amount == float(mock_order.amount)
  assert result[0].discount == float(mock_order.discount)
  assert result[0].tax_amount == float(mock_order.tax_amount)
  assert result[0].paid_amount == float(mock_order.paid_amount)
  assert result[0].balance_due == float(mock_order.balance_due)
  assert result[0].status == mock_order.status
  assert len(result[0].items) == 1
  assert result[0].items[0].product_name == mock_order.items.all.return_value[0].product_name
  assert result[0].items[0].quantity == mock_order_item.quantity
  assert result[0].items[0].unit_price == float(mock_order_item.unit_price)
  assert result[0].items[0].total == float(mock_order_item.total)
