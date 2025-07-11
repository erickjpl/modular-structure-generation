import uuid

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.value_object import Primitives, ValueObject


class UuidValueObject(ValueObject):
  def __init__(self, value: str):
    super().__init__(value)

  def _ensure_value_is_valid(self, value: Primitives) -> None:
    if not isinstance(value, str):
      raise InvalidArgumentError(f"{self.__class__.__name__} must be a string")

    try:
      uuid.UUID(value)
    except ValueError as e:
      raise InvalidArgumentError(
        f"<{self.__class__.__name__}> does not allow the value <{value}>. It must be a valid UUID."
      ) from e

  @staticmethod
  def new() -> "UuidValueObject":
    return UuidValueObject(str(uuid.uuid4()))

  @property
  def value(self) -> str:
    return super().value
