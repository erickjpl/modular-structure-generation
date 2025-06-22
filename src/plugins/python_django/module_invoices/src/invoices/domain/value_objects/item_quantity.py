from src.shared.domain import InvalidArgumentError, NumberValueObject


class ItemQuantity(NumberValueObject):
  def __init__(self, value: int):
    super().__init__(value, "Item quantity cannot be empty.")

    if self._value <= 0:
      raise InvalidArgumentError("Item quantity must be positive.")
