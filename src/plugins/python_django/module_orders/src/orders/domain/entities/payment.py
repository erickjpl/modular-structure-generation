from src.orders.domain.value_objects.currency import Currency
from src.orders.domain.value_objects.issue_date import IssueDate
from src.orders.domain.value_objects.payment_id import PaymentId
from src.orders.domain.value_objects.payment_method_id import PaymentMethodId
from src.orders.domain.value_objects.total_amount import TotalAmount
from src.orders.domain.value_objects.transaction_id import TransactionId


class Payment:
  def __init__(
    self,
    payment_id: PaymentId,
    payment_method: PaymentMethodId,
    currency: Currency,
    total_amount: TotalAmount,
    payment_date: IssueDate,
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
