
from decimal import Decimal
from faker import Faker

from src.orders.domain.entities.order_item import OrderItem
from src.orders.domain.value_objects.item_quantity import ItemQuantity
from src.orders.domain.value_objects.order_item_id import OrderItemId
from src.orders.domain.value_objects.product_id import ProductId
from src.orders.domain.value_objects.product_name import ProductName
from src.orders.domain.value_objects.product_price import ProductPrice
from src.shared.domain.value_objects.uuid_value_object import UuidValueObject

fake = Faker()


class TestOrderItem:
  def test_should_calculate_subtotal(self):
    order_item = self._create_order_item(quantity=2, unit_price=Decimal("10.00"))
    assert order_item.subtotal.value == Decimal("20.00")

  def test_should_calculate_total(self):
    order_item = self._create_order_item(
      quantity=2,
      unit_price=Decimal("10.00"),
      discount_amount=Decimal("2.00"),
      tax_amount=Decimal("1.80"),
    )
    assert order_item.total.value == Decimal("19.80")

  def _create_order_item(
    self,
    quantity: int,
    unit_price: Decimal,
    discount_amount: Decimal = Decimal("0"),
    tax_amount: Decimal = Decimal("0"),
  ) -> OrderItem:
    return OrderItem(
      order_item_id=OrderItemId(UuidValueObject.new().value),
      product_id=ProductId(UuidValueObject.new().value),
      product_name=ProductName(fake.word()),
      product_sku=fake.pystr(),
      product_image_url=fake.image_url(),
      quantity=ItemQuantity(quantity),
      unit_price=ProductPrice(unit_price),
      discount_amount=discount_amount,
      tax_amount=tax_amount,
    )
