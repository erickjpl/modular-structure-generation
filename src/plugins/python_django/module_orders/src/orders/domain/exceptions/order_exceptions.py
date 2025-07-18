from src.shared.domain.exceptions.domain_exception import HTTP_409_CONFLICT, DomainException


class InvalidOrderOperationError(Exception):
  pass


class InvalidOrderStatus(DomainException):
  def __init__(self, current_status: str, new_status: str):
    super().__init__(
      detail=f"Cannot change status from {current_status} to {new_status}",
      status_code=HTTP_409_CONFLICT,
      default_message="Invalid order status transition",
      extra_data={
        "current_status": current_status,
        "new_status": new_status,
        "allowed_transitions": ["draft", "pending"],
      },
    )
