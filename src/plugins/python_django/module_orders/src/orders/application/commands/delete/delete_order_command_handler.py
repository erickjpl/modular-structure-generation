from src.orders.application.commands.delete.delete_order_command import DeleteOrderCommand
from src.orders.application.commands.delete.order_deleter_service import OrderDeleterService
from src.shared.domain.commands.command_handler import CommandHandler


class DeleteOrderCommandHandler(CommandHandler):
  def __init__(self, service: OrderDeleterService):
    self.deleter = service

  def subscribed_to(self) -> type[DeleteOrderCommand]:
    return DeleteOrderCommand

  def handle(self, command: DeleteOrderCommand) -> None:
    self.deleter.run(command.order_id)
