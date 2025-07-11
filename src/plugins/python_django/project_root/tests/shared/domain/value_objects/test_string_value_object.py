import pytest

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.string_value_object import StringValueObject


class TestStringValueObject:
  def test_should_create_string_value_object_with_valid_string_value(self):
    value = "hello world"

    string_vo = StringValueObject(value)

    assert string_vo.value == value
    assert isinstance(string_vo.value, str)

  def test_should_raise_invalid_argument_error_for_none_value(self):
    value = None

    with pytest.raises(InvalidArgumentError, match="Value must be defined"):
      StringValueObject(value)

  def test_should_raise_invalid_argument_error_for_non_string_value(self):
    invalid_int_value = 123
    invalid_bool_value = True
    invalid_float_value = 1.23

    expected_error_regex = r"StringValueObject must be a string"

    with pytest.raises(InvalidArgumentError, match=expected_error_regex):
      StringValueObject(invalid_int_value)

    with pytest.raises(InvalidArgumentError, match=expected_error_regex):
      StringValueObject(invalid_bool_value)

    with pytest.raises(InvalidArgumentError, match=expected_error_regex):
      StringValueObject(invalid_float_value)

  def test_should_be_equal_to_another_string_value_object_with_same_value(self):
    vo1 = StringValueObject("test")
    vo2 = StringValueObject("test")

    assert vo1 == vo2
    assert vo1.equals(vo2)

  def test_should_not_be_equal_to_another_string_value_object_with_different_value(self):
    vo1 = StringValueObject("test1")
    vo2 = StringValueObject("test2")

    assert vo1 != vo2
    assert not vo1.equals(vo2)

  def test_should_not_be_equal_to_non_value_object_instance(self):
    vo = StringValueObject("test")
    non_vo = "test"

    assert vo != non_vo

  def test_hash_functionality(self):
    vo1 = StringValueObject("test_hash")
    vo2 = StringValueObject("test_hash")
    vo3 = StringValueObject("another_hash")

    assert hash(vo1) == hash(vo2)
    assert hash(vo1) != hash(vo3)
    assert len({vo1, vo2, vo3}) == 2

  def test_string_representation(self):
    value = "repr_test"
    string_vo = StringValueObject(value)

    assert str(string_vo) == value
