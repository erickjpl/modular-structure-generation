from rest_framework.permissions import AllowAny

from src.orders.application.commands.update.order_updater_service import OrderUpdaterService
from src.orders.application.commands.update.update_order_command import UpdateOrderCommand
from src.orders.application.commands.update.update_order_command_handler import UpdateOrderCommandHandler
from src.orders.infrastructure.persistences.django_order_repository import DjangoOrderRepository
from src.shared.infrastructure.api.views.update_api_view import UpdateAPIView


class UpdateOrderView(UpdateAPIView):
  permission_classes = [AllowAny]
  repositories = [("order_repository", DjangoOrderRepository)]
  application_command = UpdateOrderCommand
  application_command_handler = UpdateOrderCommandHandler
  application_service = OrderUpdaterService
  infrastructure_event_bus = None
