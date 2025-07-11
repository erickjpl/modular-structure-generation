import asyncio
import logging
from typing import Any

from src.shared.domain.events.domain_event import DomainEvent
from src.shared.domain.events.event_bus import EventBus
from src.shared.infrastructure.event_bus.domain_event_subscribers import DomainEventSubscribers

logger = logging.getLogger(__name__)


class InMemoryAsyncEventBus(EventBus):
  def __init__(self):
    self._handlers: dict[str, list[Any]] = {}

  def publish(self, events: list[DomainEvent]) -> None:
    tasks = []
    for event in events:
      if event.event_name in self._handlers:
        for handler_func in self._handlers[event.event_name]:
          tasks.append(handler_func(event))
      else:
        logger.warning(f"Advertencia: No hay suscriptores para el evento '{event.event_name}'")
    asyncio.gather(*tasks)

  def add_subscribers(self, subscribers: DomainEventSubscribers) -> None:
    for subscriber in subscribers.items:
      for event_class in subscriber.subscribed_to():
        event_name = event_class.EVENT_NAME
        if event_name not in self._handlers:
          self._handlers[event_name] = []
        self._handlers[event_name].append(subscriber.on)
        logger.info(f"Registrado {type(subscriber).__name__} para el evento '{event_name}'")
