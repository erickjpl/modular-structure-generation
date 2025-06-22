from src.shared.domain import StringValueObject


class ProductName(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Product name cannot be empty.")
