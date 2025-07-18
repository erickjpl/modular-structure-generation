from dataclasses import dataclass

from src.shared.domain.commands.command import Command
from src.orders.domain.value_objects.order_id import OrderId


@dataclass(frozen=True)
class DeleteOrderCommand(Command):
  order_id: OrderId
