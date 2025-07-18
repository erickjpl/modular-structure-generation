from decimal import Decimal

import pytest
from faker import Faker

from src.orders.domain.value_objects.total_amount import TotalAmount
from src.shared.domain.exceptions.domain_exception import DomainException

fake = Faker()


class TestTotalAmount:
  def test_should_create_total_amount(self):
    value = Decimal(fake.pydecimal(left_digits=4, right_digits=2, positive=True))
    amount = TotalAmount(value)

    assert amount.value == value

  def test_should_raise_error_if_amount_is_not_decimal(self):
    with pytest.raises(DomainException) as excinfo:
      TotalAmount(12.5)

    assert "Amount must be a Decimal." in str(excinfo.value)

  def test_should_raise_error_if_amount_is_negative(self):
    with pytest.raises(DomainException) as excinfo:
      TotalAmount(Decimal("-100.00"))

    assert "Amount cannot be negative." in str(excinfo.value)
