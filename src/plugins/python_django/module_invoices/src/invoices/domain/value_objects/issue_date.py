from datetime import date

from src.shared.domain import DateValueObject


class IssueDate(DateValueObject):
  def __init__(self, value: date):
    if not isinstance(value, date):
      raise TypeError("Issue date must be a date object.")
