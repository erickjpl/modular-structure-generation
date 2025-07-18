from src.shared.domain.value_objects.uuid_value_object import UuidValueObject


class CustomerId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value)