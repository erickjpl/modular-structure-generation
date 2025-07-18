import uuid

import pytest
from src.orders.domain.exceptions.seller_exceptions import (
    SellerException,
    SellerNotFoundError,
    SellerValidationAttemptsExceededError,
    SellerInvalidDataFormatError,
)
from src.orders.domain.value_objects.seller_id import SellerId


def test_seller_exception():
    with pytest.raises(SellerException):
        raise SellerException("Generic seller error")


def test_seller_not_found_error():
    seller_id = SellerId(str(uuid.uuid4()))
    with pytest.raises(SellerNotFoundError) as excinfo:
        raise SellerNotFoundError(seller_id)
    assert str(excinfo.value) == f"Seller {seller_id.value} not found"


def test_seller_validation_attempts_exceeded_error():
    seller_id = SellerId(str(uuid.uuid4()))
    attempts = 3
    with pytest.raises(SellerValidationAttemptsExceededError) as excinfo:
        raise SellerValidationAttemptsExceededError(seller_id, attempts)
    assert str(excinfo.value) == f"Failed to validate seller {seller_id.value} after {attempts} attempts."


def test_seller_validation_attempts_exceeded_error_with_inner_exception():
    seller_id = SellerId(str(uuid.uuid4()))
    attempts = 5
    inner_exception = ValueError("Inner error")
    with pytest.raises(SellerValidationAttemptsExceededError) as excinfo:
        raise SellerValidationAttemptsExceededError(seller_id, attempts, inner_exception)
    assert str(excinfo.value) == f"Failed to validate seller {seller_id.value} after {attempts} attempts."
    assert excinfo.value.__cause__ is inner_exception


def test_seller_invalid_data_format_error():
    with pytest.raises(SellerInvalidDataFormatError) as excinfo:
        raise SellerInvalidDataFormatError()
    assert str(excinfo.value) == "Invalid seller data format in response"
