from abc import abstractmethod
from typing import Protocol

from src.shared.domain.events.domain_event import DomainEvent
from src.shared.domain.events.domain_event_subscriber import DomainEventSubscriber


class EventBus(Protocol):
  @abstractmethod
  def publish(self, events: list[DomainEvent]) -> None:
    raise NotImplementedError

  @abstractmethod
  def add_subscribers(self, subscribers: list[DomainEventSubscriber[DomainEvent]]) -> None:
    raise NotImplementedError
