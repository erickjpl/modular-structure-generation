from decimal import Decimal

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.number_value_object import NumberValueObject


class TotalAmount(NumberValueObject):
  def __init__(self, value: Decimal, currency: str = "USD"):
    super().__init__(value)
    if not isinstance(value, Decimal):
      raise InvalidArgumentError("Amount must be a Decimal.")
    if value < Decimal("0"):
      raise InvalidArgumentError("Amount cannot be negative.")
    self._currency = currency

  @property
  def currency(self) -> str:
    return self._currency
