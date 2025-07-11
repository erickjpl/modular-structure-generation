import pytest

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.number_value_object import NumberValueObject


class TestNumberValueObject:
  def test_should_create_number_value_object_with_valid_integer_value(self):
    value = 10

    number_vo = NumberValueObject(value)

    assert number_vo.value == value
    assert isinstance(number_vo.value, int)

  def test_should_create_number_value_object_with_valid_float_value(self):
    value = 10.5

    number_vo = NumberValueObject(value)

    assert number_vo.value == value
    assert isinstance(number_vo.value, float)

  def test_should_raise_invalid_argument_error_for_none_value(self):
    value = None

    with pytest.raises(InvalidArgumentError, match="Value must be defined"):
      NumberValueObject(value)

  def test_should_raise_invalid_argument_error_for_non_numeric_value(self):
    invalid_str_value = "hello"

    expected_error_regex = r"NumberValueObject must be an integer or a float"

    with pytest.raises(InvalidArgumentError, match=expected_error_regex):
      NumberValueObject(invalid_str_value)

  def test_is_bigger_than_method(self):
    vo1 = NumberValueObject(100)
    vo2 = NumberValueObject(50)
    vo3 = NumberValueObject(100)
    vo4 = NumberValueObject(150.5)

    assert vo1.is_bigger_than(vo2) is True
    assert vo4.is_bigger_than(vo1) is True
    assert vo1.is_bigger_than(vo3) is False
    assert vo2.is_bigger_than(vo1) is False

  def test_should_be_equal_to_another_number_value_object_with_same_value(self):
    vo1 = NumberValueObject(42)
    vo2 = NumberValueObject(42)
    vo3 = NumberValueObject(42.0)

    assert vo1 == vo2
    assert vo1.equals(vo2)
    assert vo1 == vo3

  def test_should_not_be_equal_to_another_number_value_object_with_different_value(self):
    vo1 = NumberValueObject(10)
    vo2 = NumberValueObject(20)

    assert vo1 != vo2
    assert not vo1.equals(vo2)

  def test_should_not_be_equal_to_non_value_object_instance(self):
    vo = NumberValueObject(5)
    non_vo = 5

    assert vo != non_vo

  def test_hash_functionality(self):
    vo1 = NumberValueObject(77)
    vo2 = NumberValueObject(77)
    vo3 = NumberValueObject(88)

    assert hash(vo1) == hash(vo2)
    assert hash(vo1) != hash(vo3)
    assert len({vo1, vo2, vo3}) == 2

  def test_string_representation(self):
    value_int = 123
    value_float = 45.67
    vo_int = NumberValueObject(value_int)
    vo_float = NumberValueObject(value_float)

    assert str(vo_int) == str(value_int)
    assert str(vo_float) == str(value_float)

  def test_comparison_operators(self):
    vo_small = NumberValueObject(10)
    vo_medium = NumberValueObject(20)
    vo_large = NumberValueObject(30)
    vo_same = NumberValueObject(20)

    assert vo_small < vo_medium
    assert not (vo_medium < vo_small)
    assert not (vo_medium < vo_same)

    assert vo_small <= vo_medium
    assert vo_medium <= vo_same
    assert not (vo_large <= vo_medium)

    assert vo_large > vo_medium
    assert not (vo_medium > vo_large)
    assert not (vo_medium > vo_same)

    assert vo_large >= vo_medium
    assert vo_medium >= vo_same
    assert not (vo_small >= vo_medium)

    with pytest.raises(TypeError):
      _ = vo_small < 5
    with pytest.raises(TypeError):
      _ = vo_small > "abc"
