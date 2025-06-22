from src.shared.domain.value_objects.value_object import ValueObject


class NumberValueObject(ValueObject):
  def is_bigger_than(self, other: "NumberValueObject") -> bool:
    return self.value > other.value
