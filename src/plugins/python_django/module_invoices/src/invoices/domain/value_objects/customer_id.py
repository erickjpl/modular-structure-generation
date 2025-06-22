from src.shared.domain import UuidValueObject


class CustomerId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Customer id must be a valid UUID")
