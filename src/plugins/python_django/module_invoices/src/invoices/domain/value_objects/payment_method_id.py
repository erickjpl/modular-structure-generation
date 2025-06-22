from src.shared.domain import UuidValueObject


class PaymentMethodId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Payment method must be a valid UUID")
