from src.invoices.domain.value_objects import (
  Currency,
  InvoiceDate,
  PaymentId,
  PaymentMethodId,
  TotalAmount,
  TransactionId,
)


class Payment:
  def __init__(
    self,
    payment_id: PaymentId,
    payment_method: PaymentMethodId,
    currency: Currency,
    total_amount: TotalAmount,
    payment_date: InvoiceDate,
    transaction_id: TransactionId | None = None,
  ):
    self._payment_id = payment_id
    self._payment_method = payment_method
    self._currency = currency
    self._total_amount = total_amount
    self._payment_date = payment_date
    self._transaction_id = transaction_id

  def to_primitives(self) -> any:
    return {
      "payment_id": self._payment_id,
      "payment_method": self._payment_method,
      "currency": self._currency,
      "total_amount": self._total_amount,
      "payment_date": self._payment_date,
      "transaction_id": self._transaction_id,
    }
