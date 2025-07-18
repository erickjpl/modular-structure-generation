from src.shared.domain.value_objects.number_value_object import NumberValueObject


class TransactionId(NumberValueObject):
  def __init__(self, value: int):
    super().__init__(value)