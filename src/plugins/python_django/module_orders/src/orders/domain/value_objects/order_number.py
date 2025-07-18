from src.shared.domain.value_objects.string_value_object import StringValueObject


class OrderNumber(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value)