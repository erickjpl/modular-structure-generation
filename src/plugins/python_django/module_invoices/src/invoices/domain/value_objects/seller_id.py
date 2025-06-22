from src.shared.domain import UuidValueObject


class SellerId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Seller id must be a valid UUID")
