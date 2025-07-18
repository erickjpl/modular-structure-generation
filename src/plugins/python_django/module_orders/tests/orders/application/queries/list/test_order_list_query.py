from src.orders.application.queries.list.order_list_query import OrderListQuery


def test_order_list_query_creation():
  query = OrderListQuery(skip=10, limit=50)
  assert query.skip == 10
  assert query.limit == 50


def test_order_list_query_defaults():
  query = OrderListQuery()
  assert query.skip == 0
  assert query.limit == 100
