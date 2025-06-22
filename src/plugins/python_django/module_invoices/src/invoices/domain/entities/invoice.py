from datetime import date
from decimal import Decimal
from typing import list

from src.invoices.domain.entities import Customer, InvoiceLineItem, Payment
from src.invoices.domain.value_objects import (
  Currency,
  CustomerId,
  CustomerName,
  EmailAddress,
  InvoiceDate,
  InvoiceId,
  InvoiceLineItemId,
  InvoiceNumber,
  IssueDate,
  ItemQuantity,
  Money,
  PaymentId,
  ProductId,
  ProductName,
  ProductPrice,
  SellerId,
  TotalAmount,
  TransactionId,
)
from src.shared.domain import AggregateRoot, InvalidArgumentError, UuidValueObject


class Invoice(AggregateRoot):
  def __init__(
    self,
    invoice_id: InvoiceId,
    invoice_number: InvoiceNumber,
    seller_id: SellerId,
    customer_id_str: str,
    customer_name_str: str,
    customer_email_str: str,
    total_amount_primitive: Decimal,
    issue_date_primitive: date,
    transaction_id_primitive: int | None,
    is_paid: bool = False,
    line_items: list[InvoiceLineItem] | None = None,
  ):
    self._id = invoice_id
    self._invoice_number = invoice_number
    self._seller_id = seller_id
    self._is_paid = is_paid
    self._line_items: list[InvoiceLineItem] = line_items if line_items is not None else []
    self._customer = self._create_customer(customer_id_str, customer_name_str, customer_email_str)
    self._payments: list[Payment] = self._create_payment(
      total_amount_primitive, issue_date_primitive, transaction_id_primitive
    )

  def _create_customer(self, customer_id_str: str, customer_name_str: str, customer_email_str: str) -> None:
    try:
      customer_id = CustomerId(customer_id_str)
      customer_name = CustomerName(customer_name_str)
      customer_email = EmailAddress(customer_email_str)
      self._customer = Customer(customer_id, customer_name, customer_email)
    except InvalidArgumentError as e:
      raise ValueError(f"Error creating Customer for Invoice: {e}") from e

  def _create_invoice_line_items(
    self, product_id: str, product_name: str, quantity: int, currency: str, unit_price: Decimal
  ) -> None:
    try:
      invoice_line_item_id = InvoiceLineItemId(UuidValueObject.random())
      product_id = ProductId(product_id)
      product_name = ProductName(product_name)
      quantity = ItemQuantity(quantity)
      currency = Currency(currency)
      unit_price = ProductPrice(unit_price)

      new_invoice_line_item = InvoiceLineItem(
        invoice_line_item_id, product_id, product_name, quantity, currency, unit_price
      )

      self._line_items.append(new_invoice_line_item)
      self._update_total_and_payment_status()
    except InvalidArgumentError as e:
      raise ValueError(f"Error creating Payment for Invoice: {e}") from e

  def _create_payment(
    self, total_amount_primitive: Decimal, issue_date_primitive: date, transaction_id_primitive: int | None
  ) -> None:
    try:
      payment_id = PaymentId(UuidValueObject.random())
      total_amount = TotalAmount(total_amount_primitive)
      issue_date = IssueDate(issue_date_primitive)
      transaction_id = TransactionId(transaction_id_primitive)
      new_payment = Payment(payment_id, total_amount, issue_date, transaction_id)
      self._payments.append(new_payment)
      self._update_total_and_payment_status()
    except InvalidArgumentError as e:
      raise ValueError(f"Error creating Payment for Invoice: {e}") from e

  @property
  def id(self) -> int | None:
    return self._id

  def add_product_line(self, product_id: str, quantity: int, unit_price: Money):
    new_line = ProductLine(product_id, quantity, unit_price)
    self._line_items.append(new_line)
    self._update_total_and_payment_status()

  def receive_payment(self, amount: Money, payment_date: InvoiceDate, transaction_id: str | None = None):
    new_payment = Payment(amount, payment_date, transaction_id)
    self._payments.append(new_payment)
    self._update_total_and_payment_status()

  def _update_total_and_payment_status(self):
    paid_amount = sum(p.amount.amount for p in self._payments)
    if paid_amount >= self.total_amount.amount:
      self._is_paid = True
    else:
      self._is_paid = False

  def __eq__(self, other):
    if not isinstance(other, Invoice):
      return NotImplemented
    return self.id == other.id if self.id and other.id else self.invoice_number == other.invoice_number

  def __hash__(self):
    return hash(self.id) if self.id else hash(self.invoice_number)

  def __str__(self):
    return f"Invoice {self.invoice_number} (ID: {self.id})"

  def to_primitives(self) -> any:
    return {
      "invoice_id": self._invoice_id,
      "customer": {
        "id": self._customer.customer_id.value,
        "name": self._customer.name.value,
        "email": self._customer.email.value,
      },
    }
