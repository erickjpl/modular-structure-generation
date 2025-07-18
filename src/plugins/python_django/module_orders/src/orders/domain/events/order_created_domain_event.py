from datetime import datetime

from src.shared.domain.events.domain_event import DomainEvent, DomainEventAttributes


class OrderCreatedDomainEvent(DomainEvent):
  EVENT_NAME = "order.created"

  def __init__(
    self,
    *,
    aggregate_id: str,
    product_name: str,
    product_price: str,
    event_id: str | None = None,
    occurred_on: datetime | None = None,
  ):
    super().__init__(
      event_name=OrderCreatedDomainEvent.EVENT_NAME,
      aggregate_id=aggregate_id,
      event_id=event_id,
      occurred_on=occurred_on,
    )
    self._product_name = product_name
    self._product_price = product_price

  @classmethod
  def from_primitives(
    cls, *, aggregate_id: str, event_id: str, occurred_on: datetime, attributes: DomainEventAttributes
  ) -> "OrderCreatedDomainEvent":
    return cls(
      aggregate_id=aggregate_id,
      event_id=event_id,
      occurred_on=occurred_on,
      product_name=attributes["product_name"],
      product_price=attributes["product_price"],
    )

  def to_primitives(self) -> DomainEventAttributes:
    return {"product_name": self._product_name, "product_price": self._product_price}
