from rest_framework.permissions import AllowAny

from src.orders.application.commands.delete.delete_order_command import DeleteOrderCommand
from src.orders.application.commands.delete.delete_order_command_handler import DeleteOrderCommandHandler
from src.orders.application.commands.delete.order_deleter_service import OrderDeleterService
from src.orders.infrastructure.persistences.django_order_repository import DjangoOrderRepository
from src.shared.infrastructure.api.views.delete_api_view import DestroyAPIView


class DeleteOrderView(DestroyAPIView):
  permission_classes = [AllowAny]
  repositories = [("order_repository", DjangoOrderRepository)]
  application_command = DeleteOrderCommand
  application_command_handler = DeleteOrderCommandHandler
  application_service = OrderDeleterService
  infrastructure_event_bus = None
