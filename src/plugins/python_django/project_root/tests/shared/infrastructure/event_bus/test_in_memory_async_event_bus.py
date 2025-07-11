from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.shared.domain.events.domain_event import DomainEvent
from src.shared.domain.events.domain_event_subscriber import DomainEventSubscriber
from src.shared.infrastructure.event_bus.domain_event_subscribers import DomainEventSubscribers
from src.shared.infrastructure.event_bus.in_memory_async_event_bus import InMemoryAsyncEventBus


class MyDomainEvent(DomainEvent):
  EVENT_NAME = "my.domain.event"

  def __init__(self, aggregate_id: str, occurred_on: str = None):
    super().__init__(MyDomainEvent.EVENT_NAME, aggregate_id, None, occurred_on)

  @classmethod
  def from_primitives(cls, aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> "MyDomainEvent":
    return cls(aggregate_id, occurred_on)

  def to_primitives(self) -> dict:
    return {"aggregate_id": self.aggregate_id}


class AnotherDomainEvent(DomainEvent):
  EVENT_NAME = "another.domain.event"

  def __init__(self, aggregate_id: str, occurred_on: str = None):
    super().__init__(AnotherDomainEvent.EVENT_NAME, aggregate_id, None, occurred_on)

  @classmethod
  def from_primitives(cls, aggregate_id: str, body: dict, event_id: str, occurred_on: str) -> "AnotherDomainEvent":
    return cls(aggregate_id, occurred_on)

  def to_primitives(self) -> dict:
    return {"aggregate_id": self.aggregate_id}


class MySubscriber(DomainEventSubscriber):
  def subscribed_to(self) -> list[type[DomainEvent]]:
    return [MyDomainEvent]

  async def on(self, domain_event: DomainEvent):
    pass


class AnotherSubscriber(DomainEventSubscriber):
  def subscribed_to(self) -> list[type[DomainEvent]]:
    return [AnotherDomainEvent, MyDomainEvent]

  async def on(self, domain_event: DomainEvent):
    pass


class TestInMemoryAsyncEventBus:
  @pytest.fixture
  def event_bus(self):
    return InMemoryAsyncEventBus()

  @pytest.fixture
  def my_subscriber(self):
    mock_subscriber = MagicMock(spec=MySubscriber)
    mock_subscriber.on = AsyncMock()
    return mock_subscriber

  @pytest.fixture
  def another_subscriber(self):
    mock_subscriber = MagicMock(spec=AnotherSubscriber)
    mock_subscriber.on = AsyncMock()
    return mock_subscriber

  @pytest.fixture
  def domain_event_subscribers(self, my_subscriber, another_subscriber):
    return DomainEventSubscribers([my_subscriber, another_subscriber])

  @patch("asyncio.gather")
  def test_add_subscribers_registers_handlers_correctly(
    self, mock_gather, event_bus, domain_event_subscribers, my_subscriber, another_subscriber
  ):
    my_subscriber.subscribed_to.return_value = [MyDomainEvent]
    another_subscriber.subscribed_to.return_value = [AnotherDomainEvent, MyDomainEvent]

    event_bus.add_subscribers(domain_event_subscribers)

    assert MyDomainEvent.EVENT_NAME in event_bus._handlers
    assert AnotherDomainEvent.EVENT_NAME in event_bus._handlers
    assert event_bus._handlers[MyDomainEvent.EVENT_NAME] == [my_subscriber.on, another_subscriber.on]
    assert event_bus._handlers[AnotherDomainEvent.EVENT_NAME] == [another_subscriber.on]

  @patch("asyncio.gather")
  def test_publish_calls_registered_handlers(self, mock_gather, event_bus, my_subscriber, another_subscriber):
    my_event = MyDomainEvent(aggregate_id="123")
    another_event = AnotherDomainEvent(aggregate_id="456")

    event_bus._handlers[MyDomainEvent.EVENT_NAME] = [my_subscriber.on, another_subscriber.on]
    event_bus._handlers[AnotherDomainEvent.EVENT_NAME] = [another_subscriber.on]

    event_bus.publish([my_event, another_event])

    my_subscriber.on.assert_any_call(my_event)
    another_subscriber.on.assert_any_call(my_event)
    another_subscriber.on.assert_any_call(another_event)
    mock_gather.assert_called_once()

    assert my_subscriber.on.call_count == 1
    assert another_subscriber.on.call_count == 2

  @patch("asyncio.gather")
  @patch("src.shared.infrastructure.event_bus.in_memory_async_event_bus.logger")
  def test_publish_logs_warning_for_unsubscribed_event(self, mock_logger, mock_gather, event_bus):
    unsubscribed_event = MyDomainEvent(aggregate_id="789")
    event_bus._handlers = {}

    event_bus.publish([unsubscribed_event])

    mock_logger.warning.assert_called_once_with(
      f"Advertencia: No hay suscriptores para el evento '{unsubscribed_event.event_name}'"
    )
    mock_gather.assert_called_once_with()

  @patch("asyncio.gather")
  def test_publish_with_no_events(self, mock_gather, event_bus):
    event_bus.publish([])

    mock_gather.assert_called_once_with()
