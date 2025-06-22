from datetime import date
from decimal import Decimal
from typing import Protocol, TypeVar

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError

T = TypeVar("T")
Primitives = str | int | float | bool | Decimal | date


class ValueObject(Protocol):
  def __init__(self, value: Primitives, message: str | None = None):
    self._value = value
    self._ensure_value_is_defined(value, message)

  @property
  def value(self) -> str:
    return self._value

  def _ensure_value_is_defined(self, value: Primitives, message: str | None = None) -> None:
    if value is None:
      raise InvalidArgumentError(message if message is not None else "Value must be defined")

  def equals(self, other: "ValueObject") -> bool:
    return type(other) is type(self) and other.value == self._value

  def __hash__(self) -> int:
    return hash(self._value)

  def __str__(self) -> str:
    return str(self._value)

  def __eq__(self, other: object) -> bool:
    if not isinstance(other, ValueObject):
      return False
    return self.equals(other)
