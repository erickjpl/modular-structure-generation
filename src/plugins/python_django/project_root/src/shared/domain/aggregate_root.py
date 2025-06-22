from abc import ABC, abstractmethod
from typing import Any

from src.shared.domain.events.domain_event import DomainEvent


class AggregateRoot(ABC):
  def __init__(self):
    self.__domain_events: list[DomainEvent] = []

  def pull_domain_events(self) -> list[DomainEvent]:
    domain_events = self.__domain_events[:]
    self.__domain_events = []
    return domain_events

  def record(self, event: DomainEvent) -> None:
    self.__domain_events.append(event)

  @abstractmethod
  def to_primitives(self) -> Any:
    raise NotImplementedError
