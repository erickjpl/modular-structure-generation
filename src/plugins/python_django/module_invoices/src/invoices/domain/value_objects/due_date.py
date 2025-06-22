from datetime import date

from src.shared.domain import DateValueObject


class DueDate(DateValueObject):
  def __init__(self, value: date):
    if not isinstance(value, date):
      raise TypeError("Due date must be a date object.")
