from src.orders.application.queries.read.read_order_query import ReadOrderQuery

def test_read_order_query_creation():
    query = ReadOrderQuery(pk="some_pk")
    assert query.pk == "some_pk"

def test_read_order_query_empty_pk():
    query = ReadOrderQuery()
    assert query.pk is None
