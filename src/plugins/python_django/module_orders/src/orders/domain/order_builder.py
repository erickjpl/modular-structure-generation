import uuid
from datetime import date
from decimal import Decimal

from src.orders.domain.entities import Customer, Order, OrderItem, Payment
from src.orders.domain.value_objects import (
  Currency,
  CustomerEmail,
  CustomerId,
  CustomerName,
  IssueDate,
  ItemQuantity,
  OrderId,
  OrderNumber,
  PaymentId,
  ProductId,
  ProductName,
  ProductPrice,
  SellerId,
  TotalAmount,
  TransactionId,
)
from src.shared import InvalidArgumentError, UuidValueObject


class OrderBuilder:
  def __init__(self):
    self._order_id: OrderId | None = None
    self._order_number: OrderNumber | None = None
    self._seller_id: SellerId | None = None
    self._customer: Customer | None = None
    self._line_items: list[OrderItem] = []
    self._payments: list[Payment] = []
    self._issue_date: IssueDate | None = None

  def with_id(self, order_id: uuid.UUID) -> "OrderBuilder":
    self._order_id = OrderId(order_id)
    return self

  def with_order_number(self, number: str) -> "OrderBuilder":
    self._order_number = OrderNumber(number)
    return self

  def with_seller_id(self, seller_id_value: uuid.UUID) -> "OrderBuilder":
    self._seller_id = SellerId(seller_id_value)
    return self

  def for_customer(self, id_str: str, name_str: str, email_str: str) -> "OrderBuilder":
    customer_id = CustomerId(id_str)  # Asegúrate que CustomerId acepte string o el tipo correcto
    customer_name = CustomerName(name_str)
    customer_email = CustomerEmail(email_str)
    self._customer = Customer(customer_id, customer_name, customer_email)
    return self

  def with_line_item(
    self, product_id_str: str, product_name_str: str, quantity: int, unit_price_amount: Decimal, currency_str: str
  ) -> "OrderBuilder":
    product_id = ProductId(product_id_str)
    product_name = ProductName(product_name_str)
    item_quantity = ItemQuantity(quantity)
    currency = Currency(currency_str)
    unit_price_TotalAmount = TotalAmount(unit_price_amount, currency_str)
    unit_price = ProductPrice(unit_price_TotalAmount)  # Usa el Value Object ProductPrice

    line_item_id = OrderId(UuidValueObject.new())  # Genera un ID para el item
    self._line_items.append(OrderItem(line_item_id, product_id, product_name, item_quantity, currency, unit_price))
    return self

  def with_payment(
    self, amount_primitive: Decimal, payment_date_primitive: date, transaction_id_primitive: str | None = None
  ) -> "OrderBuilder":
    payment_id = PaymentId(UuidValueObject.new())  # Genera un ID para el pago
    payment_amount = TotalAmount(amount_primitive, "USD")  # Asumiendo moneda, podrías hacerla configurable
    payment_date = IssueDate(payment_date_primitive)
    transaction_id = TransactionId(transaction_id_primitive) if transaction_id_primitive else None
    self._payments.append(Payment(payment_id, payment_amount, payment_date, transaction_id))
    return self

  def with_issue_date(self, issue_date_value: date) -> "OrderBuilder":
    self._issue_date = IssueDate(issue_date_value)
    return self

  def build(self) -> Order:
    # Validaciones obligatorias al construir
    if self._customer is None:
      raise InvalidArgumentError("Order must have a customer.")
    if not self._line_items:
      raise InvalidArgumentError("Order must have at least one line item.")
    if self._order_number is None:
      raise InvalidArgumentError("Order must have an Order number.")
    if self._seller_id is None:
      raise InvalidArgumentError("Order must have a seller.")
    if self._issue_date is None:
      # Puedes poner una fecha por defecto si quieres, pero es un dato de la factura
      raise InvalidArgumentError("Order must have an issue date.")

    # Generar ID de factura si no se ha provisto
    if self._order_id is None:
      self._order_id = OrderId(UuidValueObject.new())

    # El total amount y is_paid se calculan dentro del constructor de Order
    # o cuando se llama a un método de actualización dentro de la Order.
    # Por lo tanto, no necesitamos pasarlos explícitamente desde el builder
    # si la Order tiene la lógica para calcularlos.

    return Order(
      order_id=self._order_id,
      order_number=self._order_number,
      seller_id=self._seller_id,
      customer=self._customer,
      line_items=self._line_items,
      payments=self._payments,
      # is_paid se calculará dentro del constructor de Order
      # total_amount también se calcula dentro del constructor de Order a partir de line_items
    )
