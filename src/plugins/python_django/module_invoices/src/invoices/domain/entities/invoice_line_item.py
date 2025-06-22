from decimal import Decimal

from src.invoices.domain.value_objects import (
  Currency,
  InvoiceLineItemId,
  ItemQuantity,
  ProductId,
  ProductName,
  ProductPrice,
  TotalAmount,
)


class InvoiceLineItem:
  def __init__(
    self,
    invoice_line_item_id: InvoiceLineItemId,
    product_id: ProductId,
    product_name: ProductName,
    quantity: ItemQuantity,
    currency: Currency,
    unit_price: ProductPrice,
  ):
    self._invoice_line_item_id = invoice_line_item_id
    self._product_id = product_id
    self._product_name = product_name
    self._quantity = quantity
    self._currency = currency
    self._unit_price = unit_price

  @property
  def unit_price(self) -> ProductPrice:
    return self._unit_price

  @property
  def total(self) -> TotalAmount:
    return TotalAmount(self.unit_price.amount * Decimal(self.quantity))

  def to_primitives(self) -> any:
    return {
      "invoice_line_item_id": self._invoice_line_item_id.value,
      "product_id": self._product_id.value,
      "product_name": self._product_name.value,
      "quantity": self._quantity.value,
      "currency": self._currency.value,
      "unit_price": self._unit_price.value,
      "total": self._total.value,
    }
