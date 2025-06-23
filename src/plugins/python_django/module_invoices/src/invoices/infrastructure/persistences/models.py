from django.db import models


class InvoiceModel(models.Model):
  invoice_number = models.CharField(max_length=100, unique=True)
  issue_date = models.DateField()
  customer_id = models.IntegerField()
  seller_id = models.IntegerField()
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
  is_paid = models.BooleanField(default=False)

  class Meta:
    db_table = "invoices"


class InvoiceLineItemModel(models.Model):
  invoice = models.ForeignKey(InvoiceModel, on_delete=models.CASCADE, related_name="db_line_items")
  product_id = models.CharField(max_length=255)
  quantity = models.PositiveIntegerField()
  unit_price = models.DecimalField(max_digits=10, decimal_places=2)
  line_total = models.DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    db_table = "invoice_line_items"


class PaymentModel(models.Model):
  invoice = models.ForeignKey(InvoiceModel, on_delete=models.CASCADE, related_name="db_payments")
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  payment_date = models.DateField()
  transaction_id = models.CharField(max_length=255, blank=True, null=True)

  class Meta:
    db_table = "payments"
