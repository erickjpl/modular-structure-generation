from datetime import date

from src.shared.domain.value_objects.date_value_object import DateValueObject


class DueDate(DateValueObject):
  def __init__(self, value: date):
    super().__init__(value)
    if not isinstance(value, date):
      raise TypeError("Due date must be a date object.")