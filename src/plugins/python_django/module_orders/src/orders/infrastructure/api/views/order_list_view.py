from rest_framework.permissions import AllowAny

from src.orders.application.queries.list.order_list_query import OrderListQuery
from src.orders.application.queries.list.order_list_query_handlers import OrderListQueryHandler
from src.orders.infrastructure.api.serializers.order_response_serializer import OrderResponseSerializer
from src.orders.infrastructure.persistences.django_order_repository import DjangoOrderRepository
from src.shared.infrastructure.api.views.list_api_view import ListAPIView


class OrderListView(ListAPIView):
  permission_classes = [AllowAny]
  repositories = [("repository", DjangoOrderRepository)]
  application_query = OrderListQuery
  application_query_handler = OrderListQueryHandler
  response_serializer_class = OrderResponseSerializer
