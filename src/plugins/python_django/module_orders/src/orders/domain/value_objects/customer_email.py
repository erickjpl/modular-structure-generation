import re

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.string_value_object import StringValueObject


class CustomerEmail(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value)
    if not value:
      raise InvalidArgumentError("Customer email address cannot be empty.")

    if len(self._value) > 150:
      raise InvalidArgumentError("Customer name cannot exceed 150 characters.")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", self._value):
      raise InvalidArgumentError("Invalid customer email address format.")