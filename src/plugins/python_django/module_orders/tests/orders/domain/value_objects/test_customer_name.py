
import pytest
from faker import Faker

from src.orders.domain.value_objects.customer_name import CustomerName
from src.shared.domain.exceptions.domain_exception import DomainException

fake = Faker()


class TestCustomerName:
  def test_should_create_customer_name(self):
    value = fake.name()
    name = CustomerName(value)

    assert name.value == value

  def test_should_raise_error_if_name_is_empty(self):
    with pytest.raises(DomainException) as excinfo:
      CustomerName("")

    assert "Customer name cannot be empty." in str(excinfo.value)

  def test_should_raise_error_if_name_exceeds_max_length(self):
    with pytest.raises(DomainException) as excinfo:
      CustomerName(fake.pystr(min_chars=91, max_chars=100))

    assert "Customer name cannot exceed 90 characters." in str(excinfo.value)
