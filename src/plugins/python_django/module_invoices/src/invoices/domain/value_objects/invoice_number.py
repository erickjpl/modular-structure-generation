from src.shared.domain import StringValueObject


class InvoiceNumber(StringValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Invoice number cannot be empty.")
