from django.urls import path

# from src.orders.infrastructure.api.views.create_order_view import CreateOrderView
# from src.orders.infrastructure.api.views.delete_order_view import DeleteOrderView
from src.orders.infrastructure.api.views.order_list_view import OrderListView

# from src.orders.infrastructure.api.views.read_order_view import ReadOrderView
# from src.orders.infrastructure.api.views.update_order_view import UpdateOrderView

urlpatterns = [
  path("orders", OrderListView.as_view({"get": "list"}), name="orders-list"),
  # path("orders/create", CreateOrderView.as_view({"post": "create"}), name="orders-create"),
  # path("orders/<uuid:pk>", ReadOrderView.as_view({"get": "retrieve"}), name="orders-read"),
  # path("orders/update/<uuid:pk>", UpdateOrderView.as_view({"put": "update"}), name="orders-update"),
  # path("orders/update/<uuid:pk>", UpdateOrderView.as_view({"patch": "patch"}), name="orders-patch"),
  # path("orders/delete/<uuid:pk>", DeleteOrderView.as_view({"delete": "destroy"}), name="orders-delete"),
]
