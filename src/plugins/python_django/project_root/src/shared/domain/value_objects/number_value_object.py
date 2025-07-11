from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.value_object import Primitives, ValueObject


class NumberValueObject(ValueObject):
  def __init__(self, value: int | float):
    super().__init__(value)

  def _ensure_value_is_valid(self, value: Primitives) -> None:
    if not isinstance(value, int | float):
      raise InvalidArgumentError(f"{self.__class__.__name__} must be an integer or a float")

  @property
  def value(self) -> int | float:
    return super().value

  def is_bigger_than(self, other: "NumberValueObject") -> bool:
    if not isinstance(other, NumberValueObject):
      return NotImplemented
    return self.value > other.value

  def __lt__(self, other):
    if not isinstance(other, NumberValueObject):
      return NotImplemented
    return self.value < other.value

  def __le__(self, other):
    if not isinstance(other, NumberValueObject):
      return NotImplemented
    return self.value <= other.value

  def __gt__(self, other):
    if not isinstance(other, NumberValueObject):
      return NotImplemented
    return self.value > other.value

  def __ge__(self, other):
    if not isinstance(other, NumberValueObject):
      return NotImplemented
    return self.value >= other.value
