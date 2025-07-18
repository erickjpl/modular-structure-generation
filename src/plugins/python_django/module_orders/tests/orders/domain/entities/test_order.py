
from datetime import datetime
from decimal import Decimal
from faker import Faker

import pytest

from src.orders.domain.entities.order import Order, OrderSource, OrderStatus
from src.orders.domain.entities.order_item import OrderItem
from src.orders.domain.exceptions.order_exceptions import InvalidOrderOperationError
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.order_item_id import OrderItemId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.item_quantity import ItemQuantity
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.product_id import ProductId
from src.orders.domain.value_objects.product_name import ProductName
from src.orders.domain.value_objects.product_price import ProductPrice
from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName
from src.shared.domain.value_objects.uuid_value_object import UuidValueObject

fake = Faker()


class TestOrder:
  def test_should_create_order(self):
    order = self._create_order()
    assert order.status == OrderStatus.PENDING_PAYMENT
    assert len(order.pull_domain_events()) == 1

  # def test_should_add_item_to_draft_order(self):
  #   order = self._create_order()
  #   initial_items = len(order.items)

  #   order.add_item(
  #     product_id=ProductId(UuidValueObject.new().value),
  #     product_name=ProductName(fake.word()),
  #     product_sku=fake.pystr(),
  #     product_image_url=fake.image_url(),
  #     quantity=ItemQuantity(1),
  #     unit_price=ProductPrice(Decimal("20.00")),
  #   )

  #   assert len(order.items) == initial_items + 1
  #   assert len(order.domain_events) == 2  # Created + ItemAdded

  # def test_should_not_add_item_to_non_draft_order(self):
  #   order = self._create_order(status=OrderStatus.PAID)

  #   with pytest.raises(InvalidOrderOperationError):
  #     order.add_item(
  #       product_id=ProductId(UuidValueObject.new().value),
  #       product_name=ProductName(fake.word()),
  #       product_sku=fake.pystr(),
  #       product_image_url=fake.image_url(),
  #       quantity=ItemQuantity(1),
  #       unit_price=ProductPrice(Decimal("20.00")),
  #     )

  def test_should_calculate_totals(self):
    order = self._create_order()
    assert order.total_amount.value == Decimal("10.00")

  def _create_order(self, status: OrderStatus = OrderStatus.DRAFT) -> Order:
    item = OrderItem(
      order_item_id=OrderItemId(UuidValueObject.new().value),
      product_id=ProductId(UuidValueObject.new().value),
      product_name=ProductName(fake.word()),
      product_sku=fake.pystr(),
      product_image_url=fake.image_url(),
      quantity=ItemQuantity(1),
      unit_price=ProductPrice(Decimal("10.00")),
    )

    return Order.create(
      order_id=OrderId(UuidValueObject.new().value),
      order_number=OrderNumber(fake.pystr()),
      customer_id=CustomerId(UuidValueObject.new().value),
      customer_name=CustomerName(fake.name()),
      seller_id=SellerId(UuidValueObject.new().value),
      seller_name=SellerName(fake.name()),
      ip_address=fake.ipv4(),
      source=OrderSource.WEB,
      currency="USD",
      items=[item],
    )
