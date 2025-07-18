from src.orders.application.commands.update.order_updater_service import OrderUpdaterService
from src.orders.application.commands.update.update_order_command import UpdateOrderCommand
from src.shared.domain.commands.command_handler import CommandHandler


class UpdateOrderCommandHandler(CommandHandler):
  def __init__(self, service: OrderUpdaterService):
    self.updater = service

  def subscribed_to(self) -> type[UpdateOrderCommand]:
    return UpdateOrderCommand

  def handle(self, command: UpdateOrderCommand) -> None:
    self.updater.run(
      order_id=command.order_id,
      order_number=command.order_number,
      customer_name=command.customer_name,
      seller_name=command.seller_name,
      ip_address=command.ip_address,
      source=command.source,
      status=command.status,
      currency=command.currency,
      total_amount=command.total_amount,
    )
