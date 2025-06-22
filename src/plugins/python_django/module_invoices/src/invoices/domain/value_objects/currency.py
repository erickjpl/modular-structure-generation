from src.shared.domain import StringValueObject


class Currency(StringValueObject):
  def __init__(self, value: str = "USD"):
    super().__init__(value)
