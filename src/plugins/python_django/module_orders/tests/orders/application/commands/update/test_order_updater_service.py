import uuid
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest

from src.orders.application.commands.update.order_updater_service import OrderUpdaterService
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
from src.orders.domain.value_objects.total_amount import TotalAmount
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
def mock_order_for_update(mock_order_item_for_creation):
  return Order(
    order_id=OrderId(str(uuid.uuid4())),
    order_number=Mock(value="ORD-001"),
    order_date=datetime.now(),
    customer_id=CustomerId(str(uuid.uuid4())),
    customer_name=CustomerName("Original Customer"),
    seller_id=SellerId(str(uuid.uuid4())),
    seller_name=SellerName("Original Seller"),
    ip_address="127.0.0.1",
    source=OrderSource.WEB,
    status=OrderStatus.PAID,
    currency="USD",
    items=[mock_order_item_for_creation],
  )
  mock_order_for_update._paid_amount = TotalAmount(mock_order_for_update.total_amount.value, "USD")


def test_order_updater_service_run(mock_order_repository, mock_event_bus, mock_order_for_update):
  service = OrderUpdaterService(repository=mock_order_repository, event_bus=mock_event_bus)

  mock_order_repository.get_by_id.return_value = mock_order_for_update

  updated_customer_name = CustomerName("Updated Customer")
  updated_seller_name = SellerName("Updated Seller")
  updated_ip_address = "192.168.1.100"
  updated_source = OrderSource.MOBILE
  updated_status = OrderStatus.SHIPPED
  updated_currency = "EUR"
  updated_total_amount = TotalAmount(Decimal("150.00"), "EUR")

  service.run(
    order_id=mock_order_for_update.id,
    order_number=mock_order_for_update.order_number,
    customer_name=updated_customer_name,
    seller_name=updated_seller_name,
    ip_address=updated_ip_address,
    source=updated_source,
    status=updated_status,
    currency=updated_currency,
    total_amount=updated_total_amount,
  )

  mock_order_repository.get_by_id.assert_called_once_with(mock_order_for_update.id)
  mock_order_repository.save.assert_called_once_with(mock_order_for_update)
  # Capture events after the run call, as pull_domain_events clears them
  # The service.run() method will call pull_domain_events internally
  # So we need to assert that publish was called with the events that were pulled
  # by the service.
  # Since we cannot directly access the events pulled by the service, we will
  # assert that publish was called with a list containing an OrderStatusChanged event.
  # This is a simplification for testing purposes.
  assert mock_event_bus.publish.call_args[0][0][0].__class__.__name__ == "OrderStatusChanged"

  assert mock_order_for_update.customer_name == updated_customer_name
  assert mock_order_for_update.seller_name == updated_seller_name
  assert mock_order_for_update.ip_address == updated_ip_address
  assert mock_order_for_update.source == updated_source
  assert mock_order_for_update.status == updated_status
  assert mock_order_for_update.currency == updated_currency
