from decimal import Decimal

from src.shared.domain import InvalidArgumentError, NumberValueObject


class ProductPrice(NumberValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Product price cannot be None.")

    if not isinstance(value, Decimal):
      raise InvalidArgumentError("Product price must be a Decimal.")
    if value < Decimal("0"):
      raise InvalidArgumentError("Product price cannot be negative.")
