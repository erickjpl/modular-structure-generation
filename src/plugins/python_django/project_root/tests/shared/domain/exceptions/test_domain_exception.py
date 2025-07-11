from src.shared.domain.exceptions.domain_exception import HTTP_400_BAD_REQUEST, DomainException
from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError


class TestInvalidArgumentError:
  def test_should_create_invalid_argument_error_with_correct_attributes(self):
    message = "Email format is invalid."

    error = InvalidArgumentError(message)

    assert isinstance(error, DomainException)
    assert error.detail == message
    assert error.status_code == HTTP_400_BAD_REQUEST

    assert error.default_message == f"The arguments provided by the <{InvalidArgumentError.__name__}> are not valid."
    assert error.extra_data == {}
    assert str(error) == message

  def test_should_create_invalid_argument_error_with_extra_data(self):
    message = "Password must contain a number."
    extra = {"field": "password", "min_length": 8}

    error = InvalidArgumentError(message, extra_data=extra)

    assert isinstance(error, DomainException)
    assert error.detail == message
    assert error.status_code == HTTP_400_BAD_REQUEST

    assert error.default_message == f"The arguments provided by the <{InvalidArgumentError.__name__}> are not valid."
    assert error.extra_data == extra
    assert str(error) == message

  def test_invalid_argument_error_to_dict_method(self):
    message = "Invalid age value."
    error = InvalidArgumentError(message)

    error_dict = error.to_dict()

    expected_dict = {
      "detail": "Invalid age value.",
      "status_code": HTTP_400_BAD_REQUEST,
      "message": f"The arguments provided by the <{InvalidArgumentError.__name__}> are not valid.",
      "extra_data": {},
    }
    assert error_dict == expected_dict
