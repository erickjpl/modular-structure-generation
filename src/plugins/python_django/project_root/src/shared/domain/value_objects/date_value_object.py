import datetime
from collections.abc import Callable
from datetime import date
from typing import Literal

from babel.dates import format_date

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.value_object import ValueObject


class DateValueObject(ValueObject):
  _FORMAT_PATTERNS: dict[str, str] = {
    "DD-MM-YYYY": "%d-%m-%Y",
    "DD-MM-YYYY H:i": "%d-%m-%Y %I:%M %p",
    "DD/MM/YYYY": "%d/%m/%Y",
    "DD/MM/YYYY H:i": "%d/%m/%Y %I:%M %p",
    "YYYY-MM-DD": "%Y-%m-%d",
    "YYYY-MM-DD H:i": "%Y-%m-%d %I:%M %p",
    "YYYY/MM/DD": "%Y/%m/%d",
    "YYYY/MM/DD H:i": "%Y/%m/%d %I:%M %p",
  }

  def __init__(self, value: date, message: str | None = None):
    if not isinstance(value, date):
      raise InvalidArgumentError(message if message is not None else "Value must be initialized with a date object.")
    super().__init__(value, message)
    self._date = datetime(self._value.year, self._value.month, self._value.day, 0, 0, 0)

  @property
  def value(self) -> date:
    return self._value

  def format_date_long(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self._date, format="full", locale=language)

  def format_date_short(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self._date, format="short", locale=language)

  def format_month_and_year_long(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self._date, format="MMMM yyyy", locale=language)

  def format_month_and_year_short(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self._date, format="MMM yyyy", locale=language)

  def format(
    self,
    format_type: Literal[
      "DD-MM-YYYY",
      "DD-MM-YYYY H:i",
      "DD/MM/YYYY",
      "DD/MM/YYYY H:i",
      "YYYY-MM-DD",
      "YYYY-MM-DD H:i",
      "YYYY/MM/DD",
      "YYYY/MM/DD H:i",
    ],
  ) -> str:
    formatters: dict[str, Callable[[], str]] = {
      "DD-MM-YYYY": lambda: self._date.strftime(self._FORMAT_PATTERNS["DD-MM-YYYY"]),
      "DD-MM-YYYY H:i": lambda: self._date.strftime(f"{self._FORMAT_PATTERNS['DD-MM-YYYY H:i']}"),
      "DD/MM/YYYY": lambda: self._date.strftime(self._FORMAT_PATTERNS["DD/MM/YYYY"]),
      "DD/MM/YYYY H:i": lambda: self._date.strftime(f"{self._FORMAT_PATTERNS['DD/MM/YYYY H:i']}"),
      "YYYY-MM-DD": lambda: self._date.strftime(self._FORMAT_PATTERNS["YYYY-MM-DD"]),
      "YYYY-MM-DD H:i": lambda: self._date.strftime(f"{self._FORMAT_PATTERNS['YYYY-MM-DD H:i']}"),
      "YYYY/MM/DD": lambda: self._date.strftime(self._FORMAT_PATTERNS["YYYY/MM/DD"]),
      "YYYY/MM/DD H:i": lambda: self._date.strftime(f"{self._FORMAT_PATTERNS['YYYY/MM/DD H:i']}"),
    }

    formatter = formatters.get(format_type)
    if formatter:
      return formatter()
    else:
      raise ValueError(f"Unsupported format type: {format_type}")
