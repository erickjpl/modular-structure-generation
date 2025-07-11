import pytest

from src.shared.domain.value_objects.enum_value_object import EnumValueObject, T
from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError


class UserStatus(EnumValueObject[str]):
  ACTIVE = "active"
  INACTIVE = "inactive"
  PENDING = "pending"

  _VALID_VALUES = [ACTIVE, INACTIVE, PENDING]

  def __init__(self, value: str):
    super().__init__(value, self._VALID_VALUES)

  def _throw_error_for_invalid_value(self, value: T) -> None:
    raise InvalidArgumentError(
      f"<{self.__class__.__name__}> does not allow the value <{value}>. "
      f"Allowed values are: {', '.join(self.valid_values)}"
    )


class TestEnumValueObject:
  def test_should_create_enum_value_object_with_valid_value(self):
    value = UserStatus.ACTIVE

    status = UserStatus(value)

    assert status.value == value
    assert isinstance(status.value, str)
    assert status.valid_values == [UserStatus.ACTIVE, UserStatus.INACTIVE, UserStatus.PENDING]

  def test_should_raise_invalid_argument_error_for_invalid_value(self):
    invalid_value = "deleted"
    expected_regex = r"<UserStatus> does not allow the value <deleted>. Allowed values are: active, inactive, pending"

    with pytest.raises(InvalidArgumentError, match=expected_regex):
      UserStatus(invalid_value)

  def test_should_raise_invalid_argument_error_for_none_value(self):
    value = None

    with pytest.raises(InvalidArgumentError, match="Value must be defined"):
      UserStatus(value)

  def test_should_be_equal_to_another_enum_value_object_with_same_value(self):
    vo1 = UserStatus(UserStatus.ACTIVE)
    vo2 = UserStatus(UserStatus.ACTIVE)

    assert vo1 == vo2
    assert vo1.equals(vo2)

  def test_should_not_be_equal_to_another_enum_value_object_with_different_value(self):
    vo1 = UserStatus(UserStatus.ACTIVE)
    vo2 = UserStatus(UserStatus.INACTIVE)

    assert vo1 != vo2
    assert not vo1.equals(vo2)

  def test_should_not_be_equal_to_non_value_object_instance(self):
    vo = UserStatus(UserStatus.ACTIVE)
    non_vo = "active"

    assert vo != non_vo

  def test_hash_functionality(self):
    vo1 = UserStatus(UserStatus.ACTIVE)
    vo2 = UserStatus(UserStatus.ACTIVE)
    vo3 = UserStatus(UserStatus.PENDING)

    assert hash(vo1) == hash(vo2)
    assert hash(vo1) != hash(vo3)
    assert len({vo1, vo2, vo3}) == 2

  def test_string_representation(self):
    status_value = UserStatus.INACTIVE
    status_vo = UserStatus(status_value)

    assert str(status_vo) == status_value
