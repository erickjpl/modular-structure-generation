from abc import ABC, abstractmethod

from src.invoices.domain.entities import Invoice
from src.invoices.domain.value_objects import InvoiceNumber


class IInvoiceRepository(ABC):
  @abstractmethod
  def get_by_id(self, invoice_id: int) -> Invoice | None:
    pass

  @abstractmethod
  def get_by_invoice_number(self, invoice_number: InvoiceNumber) -> Invoice | None:
    pass

  @abstractmethod
  def save(self, invoice: Invoice):
    pass
