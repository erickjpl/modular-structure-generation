import uuid
from unittest.mock import Mock

import pytest

from src.orders.application.commands.delete.delete_order_command import DeleteOrderCommand
from src.orders.application.commands.delete.delete_order_command_handler import DeleteOrderCommandHandler
from src.orders.application.commands.delete.order_deleter_service import OrderDeleterService
from src.orders.domain.value_objects.order_id import OrderId


@pytest.fixture
def mock_order_deleter_service():
  return Mock(spec=OrderDeleterService)


def test_delete_order_command_handler_subscribed_to():
  handler = DeleteOrderCommandHandler(service=Mock())
  assert handler.subscribed_to() == DeleteOrderCommand


def test_delete_order_command_handler_handle(mock_order_deleter_service):
  order_id = OrderId(str(uuid.uuid4()))
  command = DeleteOrderCommand(order_id=order_id)
  handler = DeleteOrderCommandHandler(service=mock_order_deleter_service)

  handler.handle(command)

  mock_order_deleter_service.run.assert_called_once_with(order_id)
