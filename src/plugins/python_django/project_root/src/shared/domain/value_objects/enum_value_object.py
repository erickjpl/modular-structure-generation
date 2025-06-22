from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class EnumValueObject(ABC):
  def __init__(self, value: T, valid_values: list[T]):
    self.value = value
    self.valid_values = valid_values
    self._check_value_is_valid(value)

  def _check_value_is_valid(self, value: T) -> None:
    if value not in self.valid_values:
      self._throw_error_for_invalid_value(value)

  @abstractmethod
  def _throw_error_for_invalid_value(self, value: T) -> None:
    pass
