from unittest.mock import MagicMock

import pytest

from src.shared.domain.events.domain_event_subscriber import DomainEventSubscriber
from src.shared.infrastructure.event_bus.domain_event_subscribers import DomainEventSubscribers


# --- Dummies and Mocks ---
class MockDomainEventSubscriber(DomainEventSubscriber):
    def subscribed_to(self) -> list[type]:
        return []

    def on(self, domain_event) -> None:
        pass


class MockContainer:
    def __init__(self, service_ids_and_definitions: dict, services: dict):
        self._service_ids_and_definitions = service_ids_and_definitions
        self._services = services

    def find_tagged_service_ids(self, tag: str) -> dict:
        if tag == "domainEventSubscriber":
            return self._service_ids_and_definitions
        return {}

    def get(self, service_id: str):
        return self._services.get(service_id)


# --- Test Class ---
class TestDomainEventSubscribers:

    def test_init_stores_items_correctly(self):
        subscriber1 = MockDomainEventSubscriber()
        subscriber2 = MockDomainEventSubscriber()
        subscribers_list = [subscriber1, subscriber2]

        subscribers_instance = DomainEventSubscribers(subscribers_list)

        assert subscribers_instance.items == subscribers_list

    def test_init_with_empty_list(self):
        subscribers_instance = DomainEventSubscribers([])

        assert subscribers_instance.items == []

    def test_from_container_retrieves_subscribers_correctly(self):
        # Arrange
        subscriber1_id = "subscriber.one"
        subscriber2_id = "subscriber.two"
        subscriber1 = MockDomainEventSubscriber()
        subscriber2 = MockDomainEventSubscriber()

        mock_container = MockContainer(
            service_ids_and_definitions={
                subscriber1_id: {"tags": [{"name": "domainEventSubscriber"}]},
                subscriber2_id: {"tags": [{"name": "domainEventSubscriber"}]},
            },
            services={
                subscriber1_id: subscriber1,
                subscriber2_id: subscriber2,
            },
        )

        # Act
        subscribers_instance = DomainEventSubscribers.from_container(mock_container)

        # Assert
        assert len(subscribers_instance.items) == 2
        assert subscriber1 in subscribers_instance.items
        assert subscriber2 in subscribers_instance.items

    def test_from_container_with_empty_container(self):
        # Arrange
        mock_container = MockContainer(service_ids_and_definitions={}, services={})

        # Act
        subscribers_instance = DomainEventSubscribers.from_container(mock_container)

        # Assert
        assert subscribers_instance.items == []
