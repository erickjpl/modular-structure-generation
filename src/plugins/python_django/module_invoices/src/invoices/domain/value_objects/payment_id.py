from src.shared.domain import UuidValueObject


class PaymentId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Payment id must be a valid UUID")
