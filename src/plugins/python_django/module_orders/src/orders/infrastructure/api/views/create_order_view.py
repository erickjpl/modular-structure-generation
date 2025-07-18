from rest_framework.permissions import AllowAny

from src.orders.application.commands.create.create_order_command import CreateOrderCommand
from src.orders.application.commands.create.create_order_command_handler import CreateOrderCommandHandler
from src.orders.application.commands.create.order_creator_service import OrderCreatorService
from src.orders.infrastructure.persistences.django_order_repository import DjangoOrderRepository
from src.shared.infrastructure.api.views.create_api_view import CreateAPIView


class CreateOrderView(CreateAPIView):
  permission_classes = [AllowAny]
  repositories = [("order_repository", DjangoOrderRepository)]
  application_command = CreateOrderCommand
  application_command_handler = CreateOrderCommandHandler
  application_service = OrderCreatorService
  infrastructure_event_bus = None
