from abc import abstractmethod
from typing import Protocol, TypeVar

from src.shared.domain.events.domain_event import DomainEvent

T = TypeVar("T", bound=DomainEvent)


class DomainEventSubscriber(Protocol[T]):
  @abstractmethod
  def subscribed_to(self) -> list[type[DomainEvent]]:
    raise NotImplementedError

  @abstractmethod
  def on(self, domain_event: T) -> None:
    raise NotImplementedError
