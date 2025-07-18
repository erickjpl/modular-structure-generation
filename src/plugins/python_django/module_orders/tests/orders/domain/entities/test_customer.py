
import pytest
from faker import Faker

from src.orders.domain.entities.customer import Customer
from src.orders.domain.value_objects.customer_email import CustomerEmail
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.shared.domain.exceptions.domain_exception import DomainException
from src.shared.domain.value_objects.uuid_value_object import UuidValueObject

fake = Faker()


class TestCustomer:
  def test_should_create_customer(self):
    customer_id = CustomerId(UuidValueObject.new().value)
    name = CustomerName(fake.name())
    email = CustomerEmail(fake.email())

    customer = Customer(customer_id, name, email)

    assert customer.customer_id == customer_id
    assert customer.name == name
    assert customer.email == email

  def test_should_update_customer_name(self):
    customer_id = CustomerId(UuidValueObject.new().value)
    name = CustomerName(fake.name())
    email = CustomerEmail(fake.email())
    customer = Customer(customer_id, name, email)

    new_name = CustomerName(fake.name())
    customer.update_name(new_name)

    assert customer.name == new_name

  def test_should_raise_error_if_new_name_is_not_customer_name_object(self):
    customer_id = CustomerId(UuidValueObject.new().value)
    name = CustomerName(fake.name())
    email = CustomerEmail(fake.email())
    customer = Customer(customer_id, name, email)

    with pytest.raises(DomainException) as excinfo:
      customer.update_name(fake.name())

    assert "new_name must be a CustomerName object" in str(excinfo.value)
