from datetime import datetime

from src.orders.domain.events.order_created_domain_event import OrderCreatedDomainEvent
from src.shared.domain.events.domain_event import DomainEvent
from src.shared.domain.events.domain_event_subscriber import DomainEventSubscriber


class LogOrderCreatedSubscriber(DomainEventSubscriber):
  def subscribed_to(self) -> list[type[DomainEvent]]:
    return [OrderCreatedDomainEvent]

  def on(self, domain_event: DomainEvent) -> None:
    if isinstance(domain_event, OrderCreatedDomainEvent):
      print(f"[{datetime.now()}] SUSCRIPTOR: OrderCreatedDomainEvent recibido:")
      print(f"  - Aggregate ID: {domain_event.aggregate_id}")
      print(f"  - Event ID: {domain_event.event_id}")
      print(f"  - Occurred On: {domain_event.occurred_on}")
      print(f"  - Details: {domain_event.to_primitives()}")
    else:
      print(f"[{datetime.now()}] SUSCRIPTOR: Evento desconocido recibido: {type(domain_event).__name__}")
