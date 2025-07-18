
import pytest
from faker import Faker

from src.orders.domain.value_objects.item_quantity import ItemQuantity
from src.shared.domain.exceptions.domain_exception import DomainException

fake = Faker()


class TestItemQuantity:
  def test_should_create_item_quantity(self):
    value = fake.random_int(min=1)
    quantity = ItemQuantity(value)

    assert quantity.value == value

  def test_should_raise_error_if_quantity_is_not_positive(self):
    with pytest.raises(DomainException) as excinfo:
      ItemQuantity(0)

    assert "Item quantity must be positive." in str(excinfo.value)

    with pytest.raises(DomainException) as excinfo:
      ItemQuantity(-1)

    assert "Item quantity must be positive." in str(excinfo.value)
