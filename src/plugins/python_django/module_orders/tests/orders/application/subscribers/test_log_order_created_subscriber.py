import uuid
from datetime import datetime
from unittest.mock import patch

from src.orders.application.subscribers.log_order_created_subscriber import LogOrderCreatedSubscriber
from src.orders.domain.events.order_created_domain_event import OrderCreatedDomainEvent
from src.shared.domain.events.domain_event import DomainEvent


def test_log_order_created_subscriber_subscribed_to():
  subscriber = LogOrderCreatedSubscriber()
  assert subscriber.subscribed_to() == [OrderCreatedDomainEvent]


def test_log_order_created_subscriber_on_order_created_event():
  subscriber = LogOrderCreatedSubscriber()
  order_id = str(uuid.uuid4())
  product_name = "Test Product"
  product_price = "100.00"

  event = OrderCreatedDomainEvent(
    aggregate_id=order_id,
    product_name=product_name,
    product_price=product_price,
  )

  with patch("builtins.print") as mock_print:
    subscriber.on(event)

    mock_print.assert_any_call(f"  - Aggregate ID: {order_id}")
    mock_print.assert_any_call(f"  - Event ID: {event.event_id}")
    mock_print.assert_any_call(f"  - Occurred On: {event.occurred_on}")
    mock_print.assert_any_call(f"  - Details: {event.to_primitives()}")
    # Assert that the first print call contains the expected static parts and a timestamp
    first_call_args = mock_print.call_args_list[0].args[0]
    assert "SUSCRIPTOR: OrderCreatedDomainEvent recibido:" in first_call_args
    assert first_call_args.startswith("[") and first_call_args.endswith(
      "] SUSCRIPTOR: OrderCreatedDomainEvent recibido:"
    )
    # Check if the timestamp part is roughly correct (e.g., contains year, month, day)
    assert len(first_call_args.split("]")[0]) > len("[YYYY-MM-DD HH:MM]")  # Check for more precise timestamp


def test_log_order_created_subscriber_on_unknown_event():
  subscriber = LogOrderCreatedSubscriber()

  class UnknownEvent(DomainEvent):
    def __init__(self):
      super().__init__(event_name="unknown.event", aggregate_id=str(uuid.uuid4()))

    def to_primitives(self):
      return {}

    @classmethod
    def from_primitives(cls, *, aggregate_id: str, event_id: str, occurred_on: datetime, attributes: dict):
      return cls()

  event = UnknownEvent()

  with patch("builtins.print") as mock_print:
    subscriber.on(event)

    # Assert that the print call contains the expected static parts and a timestamp
    first_call_args = mock_print.call_args_list[0].args[0]
    assert "SUSCRIPTOR: Evento desconocido recibido: UnknownEvent" in first_call_args
    assert first_call_args.startswith("[") and first_call_args.endswith(
      "] SUSCRIPTOR: Evento desconocido recibido: UnknownEvent"
    )
    # Check if the timestamp part is roughly correct
    assert len(first_call_args.split("]")[0]) > len("[YYYY-MM-DD HH:MM]")
