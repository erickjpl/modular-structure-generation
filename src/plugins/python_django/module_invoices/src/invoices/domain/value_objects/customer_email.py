import re

from src.shared.domain import InvalidArgumentError, StringValueObject


class EmailAddress(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Customer email address cannot be empty.")

    if len(self._value) > 150:
      raise InvalidArgumentError("Customer name cannot exceed 150 characters.")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", self._value):
      raise InvalidArgumentError("Invalid customer email address format.")
