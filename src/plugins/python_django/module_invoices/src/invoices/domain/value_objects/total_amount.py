from decimal import Decimal

from src.shared.domain import InvalidArgumentError, NumberValueObject


class TotalAmount(NumberValueObject):
  def __init__(self, value: Decimal):
    super().__init__(value, "Total amount cannot be None.")

    if not isinstance(value, Decimal):
      raise InvalidArgumentError("Amount must be a Decimal.")
    if value < Decimal("0"):
      raise InvalidArgumentError("Amount cannot be negative.")
