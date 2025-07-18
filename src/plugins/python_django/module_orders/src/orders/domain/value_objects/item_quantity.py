from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.number_value_object import NumberValueObject


class ItemQuantity(NumberValueObject):
  def __init__(self, value: int):
    super().__init__(value)
    if value <= 0:
      raise InvalidArgumentError("Item quantity must be positive.")