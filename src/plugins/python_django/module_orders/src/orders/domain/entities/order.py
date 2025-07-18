from datetime import datetime
from decimal import Decimal
from enum import Enum

from src.orders.domain.entities.order_item import OrderItem
from src.orders.domain.entities.payment import Payment
from src.orders.domain.events.domain_events import (
  OrderCreated,
  OrderItemAdded,
  OrderItemRemoved,
  OrderStatusChanged,
  PaymentReceived,
)
from src.orders.domain.exceptions.order_exceptions import InvalidOrderOperationError
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
from src.orders.domain.value_objects.total_amount import TotalAmount
from src.orders.domain.value_objects.transaction_id import TransactionId
from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.value_objects.invalid_argument_error import InvalidArgumentError
from src.shared.domain.value_objects.uuid_value_object import UuidValueObject


class OrderStatus(Enum):
  DRAFT = "draft"
  PENDING_PAYMENT = "pending_payment"
  PARTIALLY_PAID = "partially_paid"
  PAID = "paid"
  SHIPPED = "shipped"
  DELIVERED = "delivered"
  CANCELLED = "cancelled"
  REFUNDED = "refunded"


class OrderSource(Enum):
  WEB = "web"
  MOBILE = "mobile"


class Order(AggregateRoot):
  def __init__(
    self,
    order_id: OrderId,
    order_number: OrderNumber,
    order_date: datetime,
    customer_id: CustomerId,
    customer_name: CustomerName,
    seller_id: SellerId,
    seller_name: SellerName,
    ip_address: str,
    source: OrderSource,
    status: OrderStatus,
    currency: str,
    items: list[OrderItem],
    payments: list[Payment] | None = None,
    notes: str | None = None,
  ):
    super().__init__()
    if not items:
      raise InvalidArgumentError("An Order must have at least one line item.")

    self._id = order_id
    self._order_number = order_number
    self._order_date = order_date
    self._customer_id = customer_id
    self._customer_name = customer_name
    self._seller_id = seller_id
    self._seller_name = seller_name
    self._ip_address = ip_address
    self._source = source
    self._status = status
    self._currency = currency
    self._items = items
    self._payments = payments if payments is not None else []
    self._notes = notes

    self._update_totals_and_status()

  @property
  def id(self) -> OrderId:
    return self._id

  @property
  def order_number(self) -> OrderNumber:
    return self._order_number

  @property
  def order_date(self) -> datetime:
    return self._order_date

  @property
  def customer_id(self) -> CustomerId:
    return self._customer_id

  @property
  def customer_name(self) -> CustomerName:
    return self._customer_name

  @property
  def seller_id(self) -> SellerId:
    return self._seller_id

  @property
  def seller_name(self) -> SellerName:
    return self._seller_name

  @property
  def ip_address(self) -> str:
    return self._ip_address

  @property
  def source(self) -> OrderSource:
    return self._source

  @property
  def status(self) -> OrderStatus:
    return self._status

  @property
  def currency(self) -> str:
    return self._currency

  @property
  def items(self) -> list[OrderItem]:
    return self._items.copy()

  @property
  def payments(self) -> list[Payment]:
    return self._payments.copy()

  @property
  def notes(self) -> str | None:
    return self._notes

  @property
  def total_items(self) -> int:
    return len(self._items)

  @property
  def subtotal(self) -> TotalAmount:
    return TotalAmount(sum((item.subtotal.value for item in self._items), Decimal("0")), self._currency)

  @property
  def total_discount(self) -> TotalAmount:
    return TotalAmount(sum((item.discount_amount for item in self._items), Decimal("0")), self._currency)

  @property
  def total_tax(self) -> TotalAmount:
    return TotalAmount(sum((item.tax_amount for item in self._items), Decimal("0")), self._currency)

  @property
  def total_amount(self) -> TotalAmount:
    return TotalAmount(sum((item.total.value for item in self._items), Decimal("0")), self._currency)

  @property
  def paid_amount(self) -> TotalAmount:
    return TotalAmount(sum((payment.amount.value for payment in self._payments), Decimal("0")), self._currency)

  @property
  def balance_due(self) -> TotalAmount:
    return TotalAmount(self.total_amount.value - self.paid_amount.value, self._currency)

  def add_item(
    self,
    product_id: ProductId,
    product_name: ProductName,
    product_sku: str,
    product_image_url: str,
    quantity: ItemQuantity,
    unit_price: ProductPrice,
    discount_amount: Decimal = Decimal("0"),
    tax_amount: Decimal = Decimal("0"),
    notes: str | None = None,
  ):
    if self._status != OrderStatus.DRAFT:
      raise InvalidOrderOperationError("Cannot add items to a non-draft order")

    new_item_id = OrderItemId(UuidValueObject.new())
    new_item = OrderItem(
      order_item_id=new_item_id,
      product_id=product_id,
      product_name=product_name,
      product_sku=product_sku,
      product_image_url=product_image_url,
      quantity=quantity,
      unit_price=unit_price,
      discount_amount=discount_amount,
      tax_amount=tax_amount,
      notes=notes,
    )
    self._items.append(new_item)
    self._update_totals_and_status()
    self.record(
      OrderItemAdded(
        order_id=self._id.value,
        order_item_id=new_item_id.value,
        product_id=product_id.value,
        quantity=quantity.value,
        unit_price=float(unit_price.amount),
      )
    )

  def remove_item(self, order_item_id: OrderItemId):
    if self._status != OrderStatus.DRAFT:
      raise InvalidOrderOperationError("Cannot remove items from a non-draft order")

    item_to_remove = next((item for item in self._items if item.order_item_id == order_item_id), None)
    if item_to_remove:
      self._items.remove(item_to_remove)
      self._update_totals_and_status()
      self.record(OrderItemRemoved(order_id=self._id.value, order_item_id=order_item_id.value))

  def receive_payment(self, amount: TotalAmount, payment_date: IssueDate, transaction_id: TransactionId | None = None):
    if amount.currency != self._currency:
      raise InvalidArgumentError("Payment currency must match order currency")

    payment_id = PaymentId(UuidValueObject.new())
    new_payment = Payment(
      payment_id=payment_id, amount=amount, payment_date=payment_date, transaction_id=transaction_id
    )
    self._payments.append(new_payment)
    self._update_totals_and_status()
    self.record(
      PaymentReceived(
        order_id=self._id.value, payment_id=payment_id.value, amount=float(amount.amount), currency=amount.currency
      )
    )

  def update_status(self, new_status: OrderStatus):
    valid_transitions = {
      OrderStatus.DRAFT: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
      OrderStatus.PENDING_PAYMENT: [OrderStatus.PARTIALLY_PAID, OrderStatus.PAID, OrderStatus.CANCELLED],
      OrderStatus.PARTIALLY_PAID: [OrderStatus.PAID, OrderStatus.CANCELLED],
      OrderStatus.PAID: [OrderStatus.SHIPPED, OrderStatus.REFUNDED],
      OrderStatus.SHIPPED: [OrderStatus.DELIVERED, OrderStatus.REFUNDED],
    }

    if new_status not in valid_transitions.get(self._status, []):
      raise InvalidOrderOperationError(f"Invalid status transition from {self._status.value} to {new_status.value}")

    old_status = self._status
    self._status = new_status
    self.record(
      OrderStatusChanged(order_id=self._id.value, old_status=old_status.value, new_status=new_status.value)
    )

  def _update_totals_and_status(self):
    # Update payment status based on paid amount
    if self.paid_amount.value == 0:
      if self._status == OrderStatus.DRAFT and self.total_amount.value > 0:
        self._status = OrderStatus.PENDING_PAYMENT
    elif self.paid_amount.value >= self.total_amount.value:
      self._status = OrderStatus.PAID
    elif self.paid_amount.value > 0:
      self._status = OrderStatus.PARTIALLY_PAID

  def to_primitives(self) -> dict:
    return {
      "order_id": str(self._id.value),
      "order_number": self._order_number.value,
      "order_date": self._order_date.isoformat(),
      "customer": {"id": str(self._customer_id.value), "name": self._customer_name.value},
      "seller": {"id": str(self._seller_id.value), "name": self._seller_name.value},
      "ip_address": self._ip_address,
      "source": self._source.value,
      "status": self._status.value,
      "currency": self._currency,
      "total_items": self.total_items,
      "subtotal": float(self.subtotal.value),
      "total_discount": float(self.total_discount.value),
      "total_tax": float(self.total_tax.value),
      "total_amount": float(self.total_amount.value),
      "paid_amount": float(self.paid_amount.value),
      "balance_due": float(self.balance_due.value),
      "notes": self._notes,
      "items": [item.to_primitives() for item in self._items],
      "payments": [payment.to_primitives() for payment in self._payments],
    }

  @classmethod
  def create(
    cls,
    order_id: OrderId,
    order_number: OrderNumber,
    customer_id: CustomerId,
    customer_name: CustomerName,
    seller_id: SellerId,
    seller_name: SellerName,
    ip_address: str,
    source: OrderSource,
    currency: str,
    items: list[OrderItem],
  ) -> "Order":
    order = cls(
      order_id=order_id,
      order_number=order_number,
      order_date=datetime.now(),
      customer_id=customer_id,
      customer_name=customer_name,
      seller_id=seller_id,
      seller_name=seller_name,
      ip_address=ip_address,
      source=source,
      status=OrderStatus.DRAFT,
      currency=currency,
      items=items,
    )
    order.record(
      OrderCreated(
        order_id=order_id.value,
        customer_id=customer_id.value,
        total_amount=float(order.total_amount.value),
        currency=currency,
      )
    )
    return order

  def __eq__(self, other):
    if not isinstance(other, Order):
      return False
    return self._id.value == other._id.value

  def __hash__(self):
    return hash(self._id.value)
