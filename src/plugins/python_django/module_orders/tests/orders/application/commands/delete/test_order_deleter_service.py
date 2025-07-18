import uuid
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from src.orders.application.commands.delete.order_deleter_service import OrderDeleterService
from src.orders.domain.entities.order import Order, OrderSource, OrderStatus
from src.orders.domain.entities.order_item import OrderItem
from src.orders.domain.order_repository import IOrderRepository
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.item_quantity import ItemQuantity
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_item_id import OrderItemId
from src.orders.domain.value_objects.product_id import ProductId
from src.orders.domain.value_objects.product_name import ProductName
from src.orders.domain.value_objects.product_price import ProductPrice
from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName
from src.shared.domain.events.event_bus import EventBus


@pytest.fixture
def mock_order_repository():
  return Mock(spec=IOrderRepository)


@pytest.fixture
def mock_event_bus():
  return Mock(spec=EventBus)


@pytest.fixture
def mock_order_item_for_creation():
  return OrderItem(
    order_item_id=OrderItemId(str(uuid.uuid4())),
    product_id=ProductId(str(uuid.uuid4())),
    product_name=ProductName("Test Product"),
    product_sku="SKU123",
    product_image_url="http://example.com/image.jpg",
    quantity=ItemQuantity(1),
    unit_price=ProductPrice(Decimal("10.00")),
    discount_amount=Decimal("0.00"),
    tax_amount=Decimal("0.00"),
    notes="Test item notes",
  )


@pytest.fixture
def mock_order_for_creation(mock_order_item_for_creation):
  return Order(
    order_id=OrderId(str(uuid.uuid4())),
    order_number=Mock(value="ORD-001"),
    order_date=datetime.now(),
    customer_id=CustomerId(str(uuid.uuid4())),
    customer_name=CustomerName("Test Customer"),
    seller_id=SellerId(str(uuid.uuid4())),
    seller_name=SellerName("Test Seller"),
    ip_address="127.0.0.1",
    source=OrderSource.WEB,
    status=OrderStatus.DRAFT,
    currency="USD",
    items=[mock_order_item_for_creation],
  )


def test_order_deleter_service_run(mock_order_repository, mock_event_bus, mock_order_for_creation):
  service = OrderDeleterService(repository=mock_order_repository, event_bus=mock_event_bus)

  mock_order_repository.get_by_id.return_value = mock_order_for_creation

  order_id_to_delete = mock_order_for_creation.id
  service.run(order_id_to_delete)

  mock_order_repository.get_by_id.assert_called_once_with(order_id_to_delete)
  mock_order_repository.delete.assert_called_once_with(order_id_to_delete)
  mock_event_bus.publish.assert_called_once_with(mock_order_for_creation.pull_domain_events())
