from src.shared.domain import UuidValueObject


class InvoiceId(UuidValueObject):
  def __init__(self, value: str):
    super().__init__(value, "Invoice id must be a valid UUID")
