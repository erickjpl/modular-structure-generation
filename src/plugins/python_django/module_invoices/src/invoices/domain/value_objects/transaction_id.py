from src.shared.domain import NumberValueObject


class TransactionId(NumberValueObject):
  def __init__(self, value: int):
    super().__init__(value, "Transaction id cannot be empty.")
