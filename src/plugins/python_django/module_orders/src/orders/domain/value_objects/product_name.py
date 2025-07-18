from src.shared.domain.value_objects.string_value_object import StringValueObject


class ProductName(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value)