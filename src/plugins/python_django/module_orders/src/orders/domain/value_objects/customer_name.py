from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.string_value_object import StringValueObject


class CustomerName(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value)
    if not value:
      raise InvalidArgumentError("Customer name cannot be empty.")

    if len(self._value) > 90:
      raise InvalidArgumentError("Customer name cannot exceed 90 characters.")