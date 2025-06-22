from src.shared.domain import InvalidArgumentError, StringValueObject


class CustomerName(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Customer name cannot be empty.")

    if len(self._value) > 90:
      raise InvalidArgumentError("Customer name cannot exceed 90 characters.")
