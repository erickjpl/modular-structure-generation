from django.apps import AppConfig


class OrdersAPIConfig(AppConfig):
  default_auto_field = "django.db.models.BigAutoField"
  name = "src.orders.infrastructure.persistences"
  label = "orders"
  verbose_name = "Orders Module"
