from datetime import date

from src.shared.domain.value_objects.date_value_object import DateValueObject


class IssueDate(DateValueObject):
  def __init__(self, value: date):
    super().__init__(value)
    if not isinstance(value, date):
      raise TypeError("Issue date must be a date object.")