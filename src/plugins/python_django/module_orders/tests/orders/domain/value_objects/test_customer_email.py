
import pytest
from faker import Faker

from src.orders.domain.value_objects.customer_email import CustomerEmail
from src.shared.domain.exceptions.domain_exception import DomainException

fake = Faker()


class TestCustomerEmail:
  def test_should_create_customer_email(self):
    value = fake.email()
    email = CustomerEmail(value)

    assert email.value == value

  def test_should_raise_error_if_email_is_empty(self):
    with pytest.raises(DomainException) as excinfo:
      CustomerEmail("")

    assert "Customer email address cannot be empty." in str(excinfo.value)

  def test_should_raise_error_if_email_exceeds_max_length(self):
    with pytest.raises(DomainException) as excinfo:
      CustomerEmail(fake.pystr(min_chars=151, max_chars=200))

    assert "Customer name cannot exceed 150 characters." in str(excinfo.value)

  def test_should_raise_error_if_email_has_invalid_format(self):
    with pytest.raises(DomainException) as excinfo:
      CustomerEmail(fake.pystr(min_chars=10, max_chars=20))

    assert "Invalid customer email address format." in str(excinfo.value)
