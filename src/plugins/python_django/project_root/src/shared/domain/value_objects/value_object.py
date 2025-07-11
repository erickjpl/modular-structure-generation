from abc import ABC, abstractmethod
from typing import TypeVar

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError

T = TypeVar("T")
Primitives = str | int | float | bool


class ValueObject(ABC):
  _value: Primitives

  def __init__(self, value: Primitives):
    self._ensure_value_is_defined(value)
    self._value = value
    self._ensure_value_is_valid(value)

  @property
  def value(self) -> Primitives:
    return self._value

  def _ensure_value_is_defined(self, value: Primitives) -> None:
    if value is None:
      raise InvalidArgumentError("Value must be defined")

  @abstractmethod
  def _ensure_value_is_valid(self, value: Primitives) -> None:
    pass

  def equals(self, other: "ValueObject") -> bool:
    return type(other) is type(self) and other.value == self.value

  def __hash__(self) -> int:
    return hash(self.value)

  def __str__(self) -> str:
    return str(self.value)

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, ValueObject):
      return False
    return self.equals(other)
