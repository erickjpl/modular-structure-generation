import uuid
from decimal import Decimal

from src.orders.application.commands.create.create_order_command import CreateOrderCommand
from src.orders.domain.entities.order import OrderSource
from src.orders.domain.entities.order_item import OrderItem
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.item_quantity import ItemQuantity
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_item_id import OrderItemId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.product_id import ProductId
from src.orders.domain.value_objects.product_name import ProductName
from src.orders.domain.value_objects.product_price import ProductPrice
from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName


def test_create_order_command_creation():
  order_item = OrderItem(
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
  command = CreateOrderCommand(
    order_id=OrderId(str(uuid.uuid4())),
    order_number=OrderNumber("ORD-001"),
    customer_id=CustomerId(str(uuid.uuid4())),
    customer_name=CustomerName("Test Customer"),
    seller_id=SellerId(str(uuid.uuid4())),
    seller_name=SellerName("Test Seller"),
    ip_address="127.0.0.1",
    source=OrderSource.WEB,
    currency="USD",
    items=[order_item],
  )
  assert isinstance(command.order_id, OrderId)
  assert isinstance(command.customer_id, CustomerId)
  assert isinstance(command.seller_id, SellerId)
  assert command.order_number.value == "ORD-001"
  assert command.customer_name.value == "Test Customer"
  assert command.seller_name.value == "Test Seller"
  assert command.ip_address == "127.0.0.1"
  assert command.source == OrderSource.WEB
  assert command.currency == "USD"
  assert len(command.items) == 1
  assert command.items[0].product_name.value == "Test Product"
