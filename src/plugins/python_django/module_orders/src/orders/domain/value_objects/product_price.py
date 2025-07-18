from decimal import Decimal

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.number_value_object import NumberValueObject


class ProductPrice(NumberValueObject):
  def __init__(self, value: Decimal):
    super().__init__(value)
    if not isinstance(value, Decimal):
      raise InvalidArgumentError("Product price must be a Decimal.")
    if value < Decimal("0"):
      raise InvalidArgumentError("Product price cannot be negative.")