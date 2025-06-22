from src.shared.domain import UuidValueObject


class ProductId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Product must be a valid UUID.")
