from src.shared.domain import EnumValueObject, InvalidArgumentError


class InvoiceStatus(EnumValueObject[str]):
  PAID = "paid"
  PENDING = "pending"
  CANCELLED = "cancelled"

  def __init__(self, value: str):
    super().__init__(value, [self.PAID, self.PENDING, self.CANCELLED])

  def _throw_error_for_invalid_value(self, value: str) -> None:
    raise InvalidArgumentError(
      f"'{value}' is not a valid invoice status. Allowed values are: {', '.join(self.valid_values)}"
    )
