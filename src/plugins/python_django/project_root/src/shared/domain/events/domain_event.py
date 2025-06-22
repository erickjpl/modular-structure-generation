from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Protocol

from src.shared.domain.value_objects.uuid_value_object import UuidValueObject

DomainEventAttributes = dict[str, Any]


class DomainEvent(ABC):
  _EVENT_NAME: str = ""

  @classmethod
  def get_event_name(cls) -> str:
    return cls._EVENT_NAME

  def __init__(
    self, event_name: str, aggregate_id: str, event_id: str | None = None, occurred_on: datetime | None = None
  ):
    self.aggregate_id: str = aggregate_id
    self.event_id: str = event_id if event_id is not None else UuidValueObject.random().value
    self.occurred_on: datetime = occurred_on if occurred_on is not None else datetime.now()
    self.event_name: str = event_name

  @classmethod
  @abstractmethod
  def from_primitives(cls, params: dict[str, Any]) -> "DomainEvent":
    raise NotImplementedError

  @abstractmethod
  def to_primitives(self) -> DomainEventAttributes:
    raise NotImplementedError

  def __repr__(self):
    return (
      f"{self.__class__.__name__}(aggregate_id='{self.aggregate_id}', "
      f"event_id='{self.event_id}', occurred_on='{self.occurred_on.isoformat()}', "
      f"event_name='{self.event_name}')"
    )

  def __eq__(self, other):
    if not isinstance(other, DomainEvent):
      return NotImplemented
    return (
      self.aggregate_id == other.aggregate_id
      and self.event_id == other.event_id
      and self.event_name == other.event_name
      and self.occurred_on.timestamp() == other.occurred_on.timestamp()
    )


class DomainEventClass(Protocol):
  _EVENT_NAME: str

  @classmethod
  def get_event_name(cls) -> str: ...

  @classmethod
  def from_primitives(cls, params: dict[str, Any]) -> DomainEvent: ...
