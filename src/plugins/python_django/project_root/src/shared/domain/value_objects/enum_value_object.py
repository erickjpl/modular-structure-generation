from abc import ABC, abstractmethod
from typing import TypeVar

from src.shared.domain.value_objects.value_object import Primitives, ValueObject

T = TypeVar("T")


class EnumValueObject[T](ValueObject, ABC):
  valid_values: list[T]

  def __init__(self, value: T, valid_values: list[T]):
    self.valid_values = valid_values
    super().__init__(value)

  def _ensure_value_is_valid(self, value: Primitives) -> None:
    if value not in self.valid_values:
      self._throw_error_for_invalid_value(value)

  @abstractmethod
  def _throw_error_for_invalid_value(self, value: T) -> None:
    pass

  @property
  def value(self) -> T:
    return super().value

  def __str__(self) -> str:
    return str(self.value)
