from src.invoices.domain import (
  CustomerId,
  IInvoiceRepository,
  Invoice,
  InvoiceDate,
  InvoiceLineItemModel,
  InvoiceNumber,
  Money,
  Payment,
)
from src.invoices.infrastructure.persistences.models import InvoiceModel


class DjangoInvoiceRepository(IInvoiceRepository):
  def get_by_id(self, invoice_id: int) -> Invoice | None:
    try:
      # Lógica para cargar InvoiceModel y mapearlo a Invoice de dominio
      invoice_db = InvoiceModel.objects.get(id=invoice_id)
      # Aquí se haría el mapeo inverso de InvoiceModel a Invoice (incluyendo líneas y pagos)
      # Esto es la parte más compleja del repositorio
      return self._map_to_domain(invoice_db)
    except InvoiceModel.DoesNotExist:
      return None

  def get_by_invoice_number(self, invoice_number: InvoiceNumber) -> Invoice | None:
    try:
      invoice_db = InvoiceModel.objects.get(invoice_number=invoice_number.value)
      return self._map_to_domain(invoice_db)
    except InvoiceModel.DoesNotExist:
      return None

  def save(self, invoice: Invoice):
    # Lógica para mapear Invoice de dominio a InvoiceModel y guardarlo
    invoice_db = InvoiceModel.objects.get(id=invoice.id) if invoice.id else InvoiceModel()

    invoice_db.invoice_number = invoice.invoice_number.value
    invoice_db.issue_date = invoice.issue_date.value
    invoice_db.customer_id = invoice.customer_id.value  # Asumiendo CustomerId es un int
    invoice_db.seller_id = invoice.seller_id.value
    invoice_db.total_amount = invoice.total_amount.amount
    invoice_db.is_paid = invoice.is_paid
    invoice_db.save()  # Guarda la factura principal

    # Lógica para guardar/actualizar InvoiceLineItemModel y PaymentModel
    # Requiere borrar antiguos, añadir nuevos, actualizar existentes, etc.
    # Esto es clave para mantener la coherencia transaccional del agregado.
    self._save_line_items(invoice_db, invoice.line_items)
    self._save_payments(invoice_db, invoice.payments)

  def _map_to_domain(self, invoice_db: InvoiceModel) -> Invoice:
    # Implementar el mapeo de InvoiceModel y sus relacionados a Invoice (Dominio)
    # Esto puede ser complejo e implicar cargar todas las relaciones.
    line_items_domain = [
      # Mapear InvoiceLineItemModel a ProductLine
    ]
    payments_domain = [
      # Mapear PaymentModel a Payment
    ]
    return Invoice(
      invoice_id=invoice_db.id,
      invoice_number=InvoiceNumber(invoice_db.invoice_number),
      issue_date=InvoiceDate(invoice_db.issue_date),
      customer_id=CustomerId(invoice_db.customer_id),
      seller_id=CustomerId(invoice_db.seller_id),
      total_amount=Money(invoice_db.total_amount, "USD"),  # Moneda debe ser dinámica
      is_paid=invoice_db.is_paid,
      line_items=line_items_domain,
      payments=payments_domain,
    )

  def _save_line_items(self, invoice_db: InvoiceModel, line_items: list[InvoiceLineItemModel]):
    # Eliminar los que ya no están, actualizar los existentes, crear los nuevos
    pass

  def _save_payments(self, invoice_db: InvoiceModel, payments: list[Payment]):
    # Similar a _save_line_items
    pass
