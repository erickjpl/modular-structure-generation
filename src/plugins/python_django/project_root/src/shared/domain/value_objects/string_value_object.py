from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.value_object import Primitives, ValueObject


class StringValueObject(ValueObject):
  def __init__(self, value: str):
    super().__init__(value)

  def _ensure_value_is_valid(self, value: Primitives) -> None:
    if not isinstance(value, str):
      raise InvalidArgumentError(f"{self.__class__.__name__} must be a string")

  @property
  def value(self) -> str:
    return super().value
