import pytest
from src.orders.domain.exceptions.order_exceptions import InvalidOrderOperationError, InvalidOrderStatus
from src.shared.domain.exceptions.domain_exception import HTTP_409_CONFLICT

def test_invalid_order_operation_error():
    with pytest.raises(InvalidOrderOperationError):
        raise InvalidOrderOperationError("Test message")

def test_invalid_order_status():
    current_status = "draft"
    new_status = "shipped"
    with pytest.raises(InvalidOrderStatus) as excinfo:
        raise InvalidOrderStatus(current_status=current_status, new_status=new_status)

    exception = excinfo.value
    assert exception.status_code == HTTP_409_CONFLICT
    assert exception.detail == f"Cannot change status from {current_status} to {new_status}"
    assert exception.default_message == "Invalid order status transition"
    assert exception.extra_data["current_status"] == current_status
    assert exception.extra_data["new_status"] == new_status
    assert "allowed_transitions" in exception.extra_data
