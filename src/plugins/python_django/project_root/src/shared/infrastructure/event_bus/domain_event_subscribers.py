from typing import Any

from src.shared.domain.events.domain_event_subscriber import DomainEventSubscriber


class DomainEventSubscribers:
  def __init__(self, items: list[DomainEventSubscriber]):
    self.items = items

  @classmethod
  def from_container(cls, container: Any) -> "DomainEventSubscribers":
    """
    Método de clase para crear una instancia de DomainEventSubscribers
    a partir de un contenedor de inyección de dependencias.

    Args:
        container (Any): El contenedor de inyección de dependencias (mockeado aquí).
                         Debería tener un método `find_tagged_service_ids`
                         y un método `get`.

    Returns:
        DomainEventSubscribers: Una nueva instancia con los suscriptores encontrados.
    """
    # Aquí mockeamos la lógica de un contenedor de DI como node-dependency-injection.
    # En Python, esto se haría típicamente de forma diferente, por ejemplo,
    # iterando sobre una lista de suscriptores registrados explícitamente.
    subscriber_definitions = container.find_tagged_service_ids("domainEventSubscriber")
    subscribers: list[DomainEventSubscriber] = []

    for key, _definition in subscriber_definitions.items():
      domain_event_subscriber = container.get(key)
      subscribers.append(domain_event_subscriber)

    return cls(subscribers)
