from src.shared.domain.value_objects.string_value_object import StringValueObject


class Currency(StringValueObject):
  def __init__(self, value: str = "USD"):
    super().__init__(value)
