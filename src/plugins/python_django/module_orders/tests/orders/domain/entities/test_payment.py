
from datetime import date
from decimal import Decimal
from faker import Faker

from src.orders.domain.entities.payment import Payment
from src.orders.domain.value_objects.currency import Currency
from src.orders.domain.value_objects.issue_date import IssueDate
from src.orders.domain.value_objects.payment_id import PaymentId
from src.orders.domain.value_objects.payment_method_id import PaymentMethodId
from src.orders.domain.value_objects.total_amount import TotalAmount
from src.orders.domain.value_objects.transaction_id import TransactionId
from src.shared.domain.value_objects.uuid_value_object import UuidValueObject

fake = Faker()


class TestPayment:
  def test_should_create_payment(self):
    payment_id = PaymentId(UuidValueObject.new().value)
    payment_method = PaymentMethodId(UuidValueObject.new().value)
    currency = Currency("USD")
    total_amount = TotalAmount(Decimal("100.00"))
    payment_date = IssueDate(date.today())
    transaction_id = TransactionId(fake.random_int())

    payment = Payment(
      payment_id,
      payment_method,
      currency,
      total_amount,
      payment_date,
      transaction_id,
    )

    assert payment.to_primitives() == {
      "payment_id": payment_id,
      "payment_method": payment_method,
      "currency": currency,
      "total_amount": total_amount,
      "payment_date": payment_date,
      "transaction_id": transaction_id,
    }
