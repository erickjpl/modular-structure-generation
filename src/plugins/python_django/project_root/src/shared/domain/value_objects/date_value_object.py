from datetime import date, datetime, timedelta
from typing import Literal

from babel.dates import format_date

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.value_object import Primitives, ValueObject


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

  def __init__(self, value: datetime | date | str | None = None):
    if value is None:
      value = datetime.now()
    elif isinstance(value, date) and not isinstance(value, datetime):
      value = datetime(value.year, value.month, value.day, 0, 0, 0)

    super().__init__(value)

  def _ensure_value_is_valid(self, value: Primitives) -> None:
    if isinstance(value, datetime):
      return
    if isinstance(value, str):
      for pattern in self._FORMAT_PATTERNS.values():
        try:
          datetime.strptime(value, pattern)
          return
        except ValueError:
          pass

      try:
        datetime.fromisoformat(value)
        return
      except ValueError:
        pass

    raise InvalidArgumentError(
      f"<{self.__class__.__name__}> must be a datetime object or a valid date/datetime string."
    )

  @property
  def value(self) -> datetime:
    if isinstance(self._value, str):
      for pattern in self._FORMAT_PATTERNS.values():
        try:
          return datetime.strptime(self._value, pattern)
        except ValueError:
          pass
      try:
        return datetime.fromisoformat(self._value)
      except ValueError as e:
        raise InvalidArgumentError(
          f"Internal error: Stored string value '{self._value}' is not a valid datetime format."
        ) from e
    return self._value

  def to_iso_string(self) -> str:
    return self.value.isoformat()

  def add_days(self, days: int) -> "DateValueObject":
    return DateValueObject(self.value + timedelta(days=days))

  def subtract_days(self, days: int) -> "DateValueObject":
    return DateValueObject(self.value - timedelta(days=days))

  def is_after(self, other: "DateValueObject") -> bool:
    return self.value > other.value

  def is_before(self, other: "DateValueObject") -> bool:
    return self.value < other.value

  def format_date_long(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self.value.date(), format="full", locale=language)

  def format_date_short(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self.value.date(), format="short", locale=language)

  def format_month_and_year_long(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self.value.date(), format="MMMM YYYY", locale=language)

  def format_month_and_year_short(self, language: Literal["es", "en"] = "es") -> str:
    return format_date(self.value.date(), format="MMM YYYY", locale=language)

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
    pattern = self._FORMAT_PATTERNS.get(format_type)
    if pattern:
      return self.value.strftime(pattern)
    else:
      raise ValueError(f"Unsupported format type: {format_type}")
