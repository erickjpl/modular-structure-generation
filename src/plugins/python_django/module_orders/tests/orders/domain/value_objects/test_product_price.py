
from decimal import Decimal
import pytest
from faker import Faker

from src.orders.domain.value_objects.product_price import ProductPrice
from src.shared.domain.exceptions.domain_exception import DomainException

fake = Faker()


class TestProductPrice:
  def test_should_create_product_price(self):
    value = Decimal(fake.pydecimal(left_digits=2, right_digits=2, positive=True))
    price = ProductPrice(value)

    assert price.value == value

  def test_should_raise_error_if_price_is_not_decimal(self):
    with pytest.raises(DomainException) as excinfo:
      ProductPrice(12.5)

    assert "Product price must be a Decimal." in str(excinfo.value)

  def test_should_raise_error_if_price_is_negative(self):
    with pytest.raises(DomainException) as excinfo:
      ProductPrice(Decimal("-10.00"))

    assert "Product price cannot be negative." in str(excinfo.value)
