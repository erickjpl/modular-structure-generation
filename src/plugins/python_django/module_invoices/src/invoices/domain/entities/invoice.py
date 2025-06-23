import builtins
from typing import list

from src.invoices.domain.entities import Customer, InvoiceLineItem, Payment
from src.invoices.domain.value_objects import (
  InvoiceDate,
  InvoiceId,
  InvoiceNumber,
  ItemQuantity,
  Money,
  PaymentId,
  ProductId,
  ProductName,
  ProductPrice,
  SellerId,
  TransactionId,
)
from src.shared.domain import AggregateRoot, InvalidArgumentError


class Invoice(AggregateRoot):
  def __init__(
    self,
    invoice_id: InvoiceId,
    invoice_number: InvoiceNumber,
    seller_id: SellerId,
    customer: Customer,  # Recibe el Customer ya como VO
    line_items: builtins.list[InvoiceLineItem],  # Recibe la lista de Line Items ya como VO
    payments: builtins.list[Payment] | None = None,  # Recibe la lista de Payments ya como VO
    is_paid: bool = False,
  ):
    if not line_items:
      raise InvalidArgumentError("An Invoice must have at least one line item.")

    self._id = invoice_id
    self._invoice_number = invoice_number
    self._seller_id = seller_id
    self._customer = customer
    self._line_items: builtins.list[InvoiceLineItem] = line_items
    self._payments: builtins.list[Payment] = payments if payments is not None else []
    self._is_paid = is_paid  # Esto podría recalcularse al construir

    # Recalcula el estado de pago y el total basado en los items y pagos iniciales
    self._update_total_and_payment_status()

  # --- Propiedades y métodos de negocio existentes (sin cambios mayores) ---

  @property
  def id(self) -> InvoiceId:
    return self._id

  @property
  def invoice_number(self) -> InvoiceNumber:
    return self._invoice_number

  @property
  def seller_id(self) -> SellerId:
    return self._seller_id

  @property
  def customer(self) -> Customer:
    return self._customer

  @property
  def line_items(self) -> builtins.list[InvoiceLineItem]:
    return list(self._line_items)  # Devolver copia para inmutabilidad

  @property
  def payments(self) -> builtins.list[Payment]:
    return list(self._payments)  # Devolver copia

  @property
  def total_amount(self) -> Money:
    calculated_amount = sum(item.total.amount for item in self._line_items)
    # Asumimos que todos los items tienen la misma moneda, o se maneja la conversión
    # Para simplificar, tomamos la moneda del primer item o un default
    currency = self._line_items[0].unit_price.value.currency if self._line_items else "USD"
    return Money(calculated_amount, currency)

  @property
  def is_paid(self) -> bool:
    return self._is_paid

  # Métodos de negocio que modifican el estado (ya existentes en tu clase)
  def add_product_line(
    self, product_id: ProductId, product_name: ProductName, quantity: ItemQuantity, unit_price: ProductPrice
  ):
    new_line_id = InvoiceId(uuid.uuid4())  # O tu generador de ID
    new_line = InvoiceLineItem(new_line_id, product_id, product_name, quantity, unit_price)
    self._line_items.append(new_line)
    self._update_total_and_payment_status()

  def receive_payment(self, amount: Money, payment_date: InvoiceDate, transaction_id: TransactionId | None = None):
    payment_id = PaymentId(uuid.uuid4())  # O tu generador de ID
    new_payment = Payment(payment_id, amount, payment_date, transaction_id)
    self._payments.append(new_payment)
    self._update_total_and_payment_status()

  def _update_total_and_payment_status(self):
    paid_amount_sum = sum(p.amount.amount for p in self._payments)
    # La moneda debe ser la misma para la suma
    invoice_total = self.total_amount.amount
    self._is_paid = paid_amount_sum >= invoice_total

  def __eq__(self, other):
    if not isinstance(other, Invoice):
      return NotImplemented
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)

  def __str__(self):
    return f"Invoice {self.invoice_number.value} (ID: {self.id.value})"

  def to_primitives(self) -> dict:
    return {
      "invoice_id": str(self._id.value),
      "invoice_number": self._invoice_number.value,
      "seller_id": str(self._seller_id.value),
      "customer": {
        "id": str(self._customer.customer_id.value),
        "name": self._customer.name.value,
        "email": self._customer.email.value,
      },
      "total_amount": self.total_amount.amount,
      "issue_date": self.issue_date.value.isoformat(),  # Asumiendo que IssueDate es un Value Object
      "is_paid": self._is_paid,
      "line_items": [
        {
          "id": str(item.id.value),
          "product_id": str(item.product_id.value),
          "product_name": item.product_name.value,
          "quantity": item.quantity.value,
          "unit_price": item.unit_price.value.amount,
          "currency": item.unit_price.value.currency,
          "total": item.total.amount,
        }
        for item in self._line_items
      ],
      "payments": [
        {
          "id": str(payment.id.value),
          "amount": payment.amount.amount,
          "currency": payment.amount.currency,
          "payment_date": payment.payment_date.value.isoformat(),
          "transaction_id": str(payment.transaction_id.value) if payment.transaction_id else None,
        }
        for payment in self._payments
      ],
    }
