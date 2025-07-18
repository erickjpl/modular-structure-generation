from rest_framework.permissions import AllowAny

from src.orders.application.queries.read.read_order_query import ReadOrderQuery
from src.orders.application.queries.read.read_order_query_handlers import ReadOrderQueryHandler
from src.orders.infrastructure.api.serializers.order_response_serializer import OrderResponseSerializer
from src.orders.infrastructure.persistences.django_order_repository import DjangoOrderRepository
from src.shared.infrastructure.api.views.retrieve_api_view import RetrieveAPIView


class ReadOrderView(RetrieveAPIView):
  permission_classes = [AllowAny]
  repositories = [("order_repository", DjangoOrderRepository)]
  application_list_query = ReadOrderQuery
  application_list_query_handler = ReadOrderQueryHandler
  response_serializer_class = OrderResponseSerializer
