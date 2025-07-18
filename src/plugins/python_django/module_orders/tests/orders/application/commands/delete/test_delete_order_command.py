import uuid

from src.orders.application.commands.delete.delete_order_command import DeleteOrderCommand
from src.orders.domain.value_objects.order_id import OrderId


def test_delete_order_command_creation():
  order_id = OrderId(str(uuid.uuid4()))
  command = DeleteOrderCommand(order_id=order_id)
  assert command.order_id == order_id
