
import pytest
from faker import Faker

from src.orders.domain.value_objects.order_status import OrderStatus
from src.shared.domain.exceptions.domain_exception import DomainException

fake = Faker()


class TestOrderStatus:
  def test_should_create_order_status(self):
    value = fake.random_element(elements=("paid", "pending", "cancelled"))
    status = OrderStatus(value)

    assert status.value == value

  def test_should_raise_error_if_status_is_invalid(self):
    with pytest.raises(DomainException) as excinfo:
      OrderStatus(fake.pystr(min_chars=10, max_chars=20))

    assert "is not a valid Order status" in str(excinfo.value)
