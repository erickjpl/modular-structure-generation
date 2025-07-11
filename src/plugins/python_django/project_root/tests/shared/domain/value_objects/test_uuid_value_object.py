import uuid

import pytest

from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.uuid_value_object import UuidValueObject


class TestUuidValueObject:
  def test_should_create_uuid_value_object_with_valid_uuid_string(self):
    valid_uuid_str = str(uuid.uuid4())

    uuid_vo = UuidValueObject(valid_uuid_str)

    assert uuid_vo.value == valid_uuid_str
    assert isinstance(uuid_vo.value, str)

  def test_should_raise_invalid_argument_error_for_none_value(self):
    value = None

    with pytest.raises(InvalidArgumentError, match="Value must be defined"):
      UuidValueObject(value)

  def test_should_raise_invalid_argument_error_for_non_string_value(self):
    invalid_int_value = 123
    invalid_bool_value = True
    invalid_float_value = 1.23

    with pytest.raises(InvalidArgumentError, match=r"UuidValueObject must be a string"):
      UuidValueObject(invalid_int_value)

    with pytest.raises(InvalidArgumentError, match=r"UuidValueObject must be a string"):
      UuidValueObject(invalid_bool_value)

    with pytest.raises(InvalidArgumentError, match=r"UuidValueObject must be a string"):
      UuidValueObject(invalid_float_value)

  def test_should_raise_invalid_argument_error_for_invalid_uuid_format(self):
    invalid_uuid_str = "not-a-valid-uuid"
    malformed_uuid_str = "12345678-1234-1234-1234-12345678901"

    expected_error_regex = r"<UuidValueObject> does not allow the value <.*>. It must be a valid UUID."

    with pytest.raises(InvalidArgumentError, match=expected_error_regex):
      UuidValueObject(invalid_uuid_str)

    with pytest.raises(InvalidArgumentError, match=expected_error_regex):
      UuidValueObject(malformed_uuid_str)

  def test_new_method_should_generate_valid_uuid_value_object(self):
    new_uuid_vo = UuidValueObject.new()

    assert isinstance(new_uuid_vo, UuidValueObject)

    assert uuid.UUID(new_uuid_vo.value, version=4)

  def test_should_be_equal_to_another_uuid_value_object_with_same_value(self):
    test_uuid = str(uuid.uuid4())
    vo1 = UuidValueObject(test_uuid)
    vo2 = UuidValueObject(test_uuid)

    assert vo1 == vo2
    assert vo1.equals(vo2)

  def test_should_not_be_equal_to_another_uuid_value_object_with_different_value(self):
    vo1 = UuidValueObject(str(uuid.uuid4()))
    vo2 = UuidValueObject(str(uuid.uuid4()))

    assert vo1 != vo2
    assert not vo1.equals(vo2)

  def test_hash_functionality(self):
    test_uuid_1 = str(uuid.uuid4())
    test_uuid_2 = str(uuid.uuid4())
    vo1 = UuidValueObject(test_uuid_1)
    vo2 = UuidValueObject(test_uuid_1)
    vo3 = UuidValueObject(test_uuid_2)

    assert hash(vo1) == hash(vo2)
    assert hash(vo1) != hash(vo3)
    assert len({vo1, vo2, vo3}) == 2

  def test_string_representation(self):
    test_uuid = str(uuid.uuid4())
    uuid_vo = UuidValueObject(test_uuid)

    assert str(uuid_vo) == test_uuid
