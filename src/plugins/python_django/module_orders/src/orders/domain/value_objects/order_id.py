from src.shared.domain.value_objects.uuid_value_object import UuidValueObject


class OrderId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value)
