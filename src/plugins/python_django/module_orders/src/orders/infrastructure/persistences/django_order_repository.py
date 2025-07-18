from decimal import Decimal

from django.db import transaction

from src.orders.domain.entities.order import Order, OrderSource, OrderStatus
from src.orders.domain.entities.order_item import OrderItem
from src.orders.domain.entities.payment import Payment
from src.orders.domain.order_repository import IOrderRepository
from src.orders.domain.value_objects.customer_id import CustomerId
from src.orders.domain.value_objects.customer_name import CustomerName
from src.orders.domain.value_objects.issue_date import IssueDate
from src.orders.domain.value_objects.item_quantity import ItemQuantity
from src.orders.domain.value_objects.order_id import OrderId
from src.orders.domain.value_objects.order_item_id import OrderItemId
from src.orders.domain.value_objects.order_number import OrderNumber
from src.orders.domain.value_objects.payment_id import PaymentId
from src.orders.domain.value_objects.product_id import ProductId
from src.orders.domain.value_objects.product_name import ProductName
from src.orders.domain.value_objects.product_price import ProductPrice
from src.orders.domain.value_objects.seller_id import SellerId
from src.orders.domain.value_objects.seller_name import SellerName
from src.orders.infrastructure.persistences.models.order import OrderDAO
from src.orders.infrastructure.persistences.models.order_item import OrderItemDAO


class DjangoOrderRepository(IOrderRepository):
  def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
    order_daos = OrderDAO.objects.prefetch_related("items").all()[skip : skip + limit]
    return [self._to_domain_entity(dao) for dao in order_daos]

  def get_by_id(self, order_id: OrderId) -> Order | None:
    try:
      order_db = OrderDAO.objects.prefetch_related("items").get(id=order_id.value)
      return self._to_domain_entity(order_db)
    except OrderDAO.DoesNotExist:
      return None

  def get_by_order_number(self, order_number: OrderNumber) -> Order | None:
    try:
      order_db = OrderDAO.objects.prefetch_related("items").get(order_number=order_number.value)
      return self._to_domain_entity(order_db)
    except OrderDAO.DoesNotExist:
      return None

  def delete(self, order_id: OrderId) -> None:
    OrderDAO.objects.filter(id=order_id.value).delete()

  @transaction.atomic
  def save(self, order: Order) -> None:
    order_db = self._get_or_create_order_dao(order)
    self._save_order_items(order_db, order.line_items)
    self._save_order_payments(order_db, order.payments)

  def _get_or_create_order_dao(self, order: Order) -> OrderDAO:
    defaults = {
      "order_number": order.order_number.value,
      "order_date": order.order_date.value,
      "customer_id": order.customer_id.value,
      "seller_id": order.seller_id.value,
      "total_amount": float(order.total_amount.amount),
      "discount_amount": float(order.total_discount.amount),
      "tax_amount": float(order.total_tax.amount),
      "paid_amount": float(order.paid_amount.amount),
      "status": order.status.value,
      "notes": order.notes,
    }

    if order.id:
      order_db, created = OrderDAO.objects.update_or_create(id=order.id.value, defaults=defaults)
    else:
      order_db = OrderDAO.objects.create(**defaults)

    return order_db

  def _save_order_items(self, order_db: OrderDAO, items: list[OrderItem]) -> None:
    existing_item_ids = [item.id.value for item in items if item.id]
    OrderItemDAO.objects.filter(order=order_db).exclude(id__in=existing_item_ids).delete()

    for item in items:
      defaults = {
        "product_id": item.product_id.value,
        "product_name": item.product_name.value,
        "product_sku": item.product_sku,
        "product_image_url": item.product_image_url,
        "quantity": item.quantity.value,
        "unit_price": float(item.unit_price.amount),
        "subtotal": float(item.subtotal.amount),
        "discount_amount": float(item.discount_amount),
        "tax_amount": float(item.tax_amount),
        "total": float(item.total.amount),
        "notes": item.notes,
      }

      if item.id:
        OrderItemDAO.objects.update_or_create(id=item.id.value, order=order_db, defaults=defaults)
      else:
        OrderItemDAO.objects.create(order=order_db, **defaults)

  def _save_order_payments(self, order_db: OrderDAO, payments: list[Payment]) -> None:
    """Guarda los pagos de la orden"""
    # Similar a _save_order_items
    # existing_payment_ids = [payment.id.value for payment in payments if payment.id]
    # PaymentDAO.objects.filter(order=order_db).exclude(id__in=existing_payment_ids).delete()

    # for payment in payments:
    #   defaults = {
    #     "amount": float(payment.amount.amount),
    #     "payment_date": payment.payment_date.value,
    #     "payment_method": payment.payment_method.value,
    #     "transaction_id": payment.transaction_id.value if payment.transaction_id else None,
    #     "notes": payment.notes,
    #   }

    #   if payment.id:
    #     PaymentDAO.objects.update_or_create(id=payment.id.value, order=order_db, defaults=defaults)
    #   else:
    #     PaymentDAO.objects.create(order=order_db, **defaults)

  def _to_domain_entity(self, order_db: OrderDAO) -> Order:
    items = []
    for item_db in order_db.items.all():
      items.append(
        OrderItem(
          id=OrderItemId(item_db.id),
          product_id=ProductId(item_db.product_id),
          product_name=ProductName(item_db.product_name),
          product_sku=item_db.product_sku,
          product_image_url=item_db.product_image_url,
          quantity=ItemQuantity(item_db.quantity),
          unit_price=ProductPrice(amount=Decimal(str(item_db.unit_price)), currency=order_db.currency),
          discount_amount=Decimal(str(item_db.discount_amount)),
          tax_amount=Decimal(str(item_db.tax_amount)),
          notes=item_db.notes,
        )
      )

    payments = []
    for payment_db in order_db.payments.all():
      payments.append(
        Payment(
          id=PaymentId(payment_db.id),
          # amount=Money(amount=Decimal(str(payment_db.amount)), currency=order_db.currency),
          payment_date=IssueDate(payment_db.payment_date),
          # payment_method=PaymentMethod(payment_db.payment_method),
          # transaction_id=TransactionId(payment_db.transaction_id) if payment_db.transaction_id else None,
          notes=payment_db.notes,
        )
      )

    return Order(
      id=OrderId(order_db.id),
      order_number=OrderNumber(order_db.order_number),
      # order_date=OrderDate(order_db.order_date),
      customer_id=CustomerId(order_db.customer_id),
      customer_name=CustomerName(order_db.customer_name) if order_db.customer_name else None,
      seller_id=SellerId(order_db.seller_id),
      seller_name=SellerName(order_db.seller_name) if order_db.seller_name else None,
      ip_address=order_db.ip_address,
      source=OrderSource(order_db.source),
      status=OrderStatus(order_db.status),
      currency=order_db.currency,
      items=items,
      payments=payments,
      notes=order_db.notes,
    )
