from datetime import date, datetime, timedelta

import pytest

from src.shared.domain.value_objects.date_value_object import DateValueObject
from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError


class TestDateValueObject:
  def test_should_create_date_value_object_with_datetime_object(self):
    now = datetime.now()

    date_vo = DateValueObject(now)

    assert date_vo.value == now
    assert isinstance(date_vo.value, datetime)

  def test_should_create_date_value_object_with_date_object(self):
    today = date(2025, 6, 28)
    expected_datetime = datetime(2025, 6, 28, 0, 0, 0)

    date_vo = DateValueObject(today)

    assert date_vo.value == expected_datetime
    assert isinstance(date_vo.value, datetime)

  @pytest.mark.parametrize(
    "input_str, expected_dt",
    [
      ("28-06-2025", datetime(2025, 6, 28, 0, 0, 0)),
      ("28-06-2025 10:30 AM", datetime(2025, 6, 28, 10, 30, 0)),
      ("28/06/2025", datetime(2025, 6, 28, 0, 0, 0)),
      ("28/06/2025 03:45 PM", datetime(2025, 6, 28, 15, 45, 0)),
      ("2025-06-28", datetime(2025, 6, 28, 0, 0, 0)),
      ("2025-06-28 23:59", datetime(2025, 6, 28, 23, 59, 0)),
      ("2025/06/28", datetime(2025, 6, 28, 0, 0, 0)),
      ("2025/06/28 01:00 AM", datetime(2025, 6, 28, 1, 0, 0)),
      ("2025-06-28T10:30:00.123456", datetime(2025, 6, 28, 10, 30, 0, 123456)),
    ],
  )
  def test_should_create_date_value_object_with_valid_string_formats(self, input_str, expected_dt: datetime):
    date_vo = DateValueObject(input_str)

    assert date_vo.value == expected_dt
    assert isinstance(date_vo.value, datetime)

  def test_should_create_date_value_object_with_none_value_defaults_to_now(self):
    date_vo = DateValueObject(None)

    current_time_after_creation = datetime.now()

    assert isinstance(date_vo.value, datetime)

    time_difference = abs(date_vo.value - current_time_after_creation)
    assert time_difference < timedelta(seconds=1)

    assert date_vo.value.year == current_time_after_creation.year
    assert date_vo.value.month == current_time_after_creation.month
    assert date_vo.value.day == current_time_after_creation.day

  def test_should_raise_invalid_argument_error_for_invalid_string_format(self):
    invalid_str = "invalid-date-string"
    expected_regex = r"<DateValueObject> must be a datetime object or a valid date/datetime string."

    with pytest.raises(InvalidArgumentError, match=expected_regex):
      DateValueObject(invalid_str)

  def test_should_raise_invalid_argument_error_for_non_date_or_string_value(self):
    invalid_int = 12345
    invalid_list = [1, 2, 3]
    expected_regex = r"<DateValueObject> must be a datetime object or a valid date/datetime string."

    with pytest.raises(InvalidArgumentError, match=expected_regex):
      DateValueObject(invalid_int)
    with pytest.raises(InvalidArgumentError, match=expected_regex):
      DateValueObject(invalid_list)

  def test_to_iso_string_method(self):
    dt = datetime(2023, 1, 15, 14, 30, 45, 123456)
    date_vo = DateValueObject(dt)

    iso_str = date_vo.to_iso_string()

    assert iso_str == dt.isoformat()

  def test_add_days_method(self):
    start_date = datetime(2024, 1, 1, 10, 0, 0)
    date_vo = DateValueObject(start_date)
    days_to_add = 5
    expected_date = datetime(2024, 1, 6, 10, 0, 0)

    new_date_vo = date_vo.add_days(days_to_add)

    assert isinstance(new_date_vo, DateValueObject)
    assert new_date_vo.value == expected_date

  def test_subtract_days_method(self):
    start_date = datetime(2024, 1, 10, 10, 0, 0)
    date_vo = DateValueObject(start_date)
    days_to_subtract = 3
    expected_date = datetime(2024, 1, 7, 10, 0, 0)

    new_date_vo = date_vo.subtract_days(days_to_subtract)

    assert isinstance(new_date_vo, DateValueObject)
    assert new_date_vo.value == expected_date

  def test_is_after_method(self):
    date1 = DateValueObject(datetime(2024, 1, 10))
    date2 = DateValueObject(datetime(2024, 1, 5))
    date3 = DateValueObject(datetime(2024, 1, 10))

    assert date1.is_after(date2) is True
    assert date2.is_after(date1) is False
    assert date1.is_after(date3) is False

  def test_is_before_method(self):
    date1 = DateValueObject(datetime(2024, 1, 10))
    date2 = DateValueObject(datetime(2024, 1, 5))
    date3 = DateValueObject(datetime(2024, 1, 10))

    assert date2.is_before(date1) is True
    assert date1.is_before(date2) is False
    assert date1.is_before(date3) is False

  @pytest.mark.parametrize(
    "input_dt, lang, expected_format",
    [
      (datetime(2025, 1, 15), "es", "miércoles, 15 de enero de 2025"),
      (datetime(2025, 1, 15), "en", "Wednesday, January 15, 2025"),
    ],
  )
  def test_format_date_long(self, input_dt, lang, expected_format):
    date_vo = DateValueObject(input_dt)
    assert date_vo.format_date_long(language=lang) == expected_format

  @pytest.mark.parametrize(
    "input_dt, lang, expected_format",
    [
      (datetime(2025, 1, 15), "es", "15/1/25"),
      (datetime(2025, 1, 15), "en", "1/15/25"),
    ],
  )
  def test_format_date_short(self, input_dt, lang, expected_format):
    date_vo = DateValueObject(input_dt)
    assert date_vo.format_date_short(language=lang) == expected_format

  @pytest.mark.parametrize(
    "input_dt, lang, expected_format",
    [
      (datetime(2025, 1, 15), "es", "enero 2025"),
      (datetime(2025, 1, 15), "en", "January 2025"),
    ],
  )
  def test_format_month_and_year_long(self, input_dt, lang, expected_format):
    date_vo = DateValueObject(input_dt)
    assert date_vo.format_month_and_year_long(language=lang) == expected_format

  @pytest.mark.parametrize(
    "input_dt, lang, expected_format",
    [
      (datetime(2025, 1, 15), "es", "ene 2025"),
      (datetime(2025, 1, 15), "en", "Jan 2025"),
    ],
  )
  def test_format_month_and_year_short(self, input_dt, lang, expected_format):
    date_vo = DateValueObject(input_dt)
    assert date_vo.format_month_and_year_short(language=lang) == expected_format

  @pytest.mark.parametrize(
    "format_type, expected_output",
    [
      ("DD-MM-YYYY", "28-06-2025"),
      ("DD-MM-YYYY H:i", "28-06-2025 10:30 AM"),
      ("DD/MM/YYYY", "28/06/2025"),
      ("DD/MM/YYYY H:i", "28/06/2025 10:30 AM"),
      ("YYYY-MM-DD", "2025-06-28"),
      ("YYYY-MM-DD H:i", "2025-06-28 10:30 AM"),
      ("YYYY/MM/DD", "2025/06/28"),
      ("YYYY/MM/DD H:i", "2025/06/28 10:30 AM"),
    ],
  )
  def test_format_method_with_valid_types(self, format_type, expected_output):
    fixed_dt = datetime(2025, 6, 28, 10, 30, 0)
    date_vo = DateValueObject(fixed_dt)

    formatted_str = date_vo.format(format_type)

    assert formatted_str == expected_output

  def test_format_method_with_unsupported_type_raises_error(self):
    date_vo = DateValueObject(datetime.now())
    unsupported_format = "UNSUPPORTED"

    with pytest.raises(ValueError, match="Unsupported format type: UNSUPPORTED"):
      date_vo.format(unsupported_format)

  def test_should_be_equal_to_another_date_value_object_with_same_value(self):
    dt = datetime(2024, 7, 1, 12, 0, 0)
    vo1 = DateValueObject(dt)
    vo2 = DateValueObject(dt)

    assert vo1 == vo2
    assert vo1.equals(vo2)

  def test_should_not_be_equal_to_another_date_value_object_with_different_value(self):
    vo1 = DateValueObject(datetime(2024, 7, 1))
    vo2 = DateValueObject(datetime(2024, 7, 2))

    assert vo1 != vo2
    assert not vo1.equals(vo2)

  def test_hash_functionality(self):
    dt1 = datetime(2024, 8, 1)
    dt2 = datetime(2024, 8, 2)
    vo1 = DateValueObject(dt1)
    vo2 = DateValueObject(dt1)
    vo3 = DateValueObject(dt2)

    assert hash(vo1) == hash(vo2)
    assert hash(vo1) != hash(vo3)
    assert len({vo1, vo2, vo3}) == 2

  def test_string_representation(self):
    dt = datetime(2024, 9, 10, 15, 30, 0)
    date_vo = DateValueObject(dt)

    assert str(date_vo) == str(dt)
