import uuid
from datetime import date
from decimal import Decimal

from .aggregates import Invoice
from .entities import Customer, InvoiceLineItem, Payment
from .value_objects import (
  Currency,
  CustomerId,
  CustomerName,
  EmailAddress,
  InvalidArgumentError,
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


class InvoiceBuilder:
  def __init__(self):
    self._invoice_id: InvoiceId | None = None
    self._invoice_number: InvoiceNumber | None = None
    self._seller_id: SellerId | None = None
    self._customer: Customer | None = None
    self._line_items: list[InvoiceLineItem] = []
    self._payments: list[Payment] = []
    self._issue_date: InvoiceDate | None = None

  def with_id(self, invoice_id: uuid.UUID) -> "InvoiceBuilder":
    self._invoice_id = InvoiceId(invoice_id)
    return self

  def with_invoice_number(self, number: str) -> "InvoiceBuilder":
    self._invoice_number = InvoiceNumber(number)
    return self

  def with_seller_id(self, seller_id_value: uuid.UUID) -> "InvoiceBuilder":
    self._seller_id = SellerId(seller_id_value)
    return self

  def for_customer(self, id_str: str, name_str: str, email_str: str) -> "InvoiceBuilder":
    customer_id = CustomerId(id_str)  # Asegúrate que CustomerId acepte string o el tipo correcto
    customer_name = CustomerName(name_str)
    customer_email = EmailAddress(email_str)
    self._customer = Customer(customer_id, customer_name, customer_email)
    return self

  def with_line_item(
    self, product_id_str: str, product_name_str: str, quantity: int, unit_price_amount: Decimal, currency_str: str
  ) -> "InvoiceBuilder":
    product_id = ProductId(product_id_str)
    product_name = ProductName(product_name_str)
    item_quantity = ItemQuantity(quantity)
    currency = Currency(currency_str)
    unit_price_money = Money(unit_price_amount, currency_str)
    unit_price = ProductPrice(unit_price_money)  # Usa el Value Object ProductPrice

    line_item_id = InvoiceId(uuid.uuid4())  # Genera un ID para el item
    self._line_items.append(InvoiceLineItem(line_item_id, product_id, product_name, item_quantity, unit_price))
    return self

  def with_payment(
    self, amount_primitive: Decimal, payment_date_primitive: date, transaction_id_primitive: str | None = None
  ) -> "InvoiceBuilder":
    payment_id = PaymentId(uuid.uuid4())  # Genera un ID para el pago
    payment_amount = Money(amount_primitive, "USD")  # Asumiendo moneda, podrías hacerla configurable
    payment_date = InvoiceDate(payment_date_primitive)
    transaction_id = TransactionId(transaction_id_primitive) if transaction_id_primitive else None
    self._payments.append(Payment(payment_id, payment_amount, payment_date, transaction_id))
    return self

  def with_issue_date(self, issue_date_value: date) -> "InvoiceBuilder":
    self._issue_date = InvoiceDate(issue_date_value)
    return self

  def build(self) -> Invoice:
    # Validaciones obligatorias al construir
    if self._customer is None:
      raise InvalidArgumentError("Invoice must have a customer.")
    if not self._line_items:
      raise InvalidArgumentError("Invoice must have at least one line item.")
    if self._invoice_number is None:
      raise InvalidArgumentError("Invoice must have an invoice number.")
    if self._seller_id is None:
      raise InvalidArgumentError("Invoice must have a seller.")
    if self._issue_date is None:
      # Puedes poner una fecha por defecto si quieres, pero es un dato de la factura
      raise InvalidArgumentError("Invoice must have an issue date.")

    # Generar ID de factura si no se ha provisto
    if self._invoice_id is None:
      self._invoice_id = InvoiceId(uuid.uuid4())

    # El total amount y is_paid se calculan dentro del constructor de Invoice
    # o cuando se llama a un método de actualización dentro de la Invoice.
    # Por lo tanto, no necesitamos pasarlos explícitamente desde el builder
    # si la Invoice tiene la lógica para calcularlos.

    return Invoice(
      invoice_id=self._invoice_id,
      invoice_number=self._invoice_number,
      seller_id=self._seller_id,
      customer=self._customer,
      line_items=self._line_items,
      payments=self._payments,
      # is_paid se calculará dentro del constructor de Invoice
      # total_amount también se calcula dentro del constructor de Invoice a partir de line_items
    )
