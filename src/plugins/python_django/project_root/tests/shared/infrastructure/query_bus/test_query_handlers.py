from unittest.mock import MagicMock

import pytest

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.query_handler import QueryHandler
from src.shared.domain.queries.query_not_registered_error import QueryNotRegisteredError
from src.shared.domain.queries.response import Response
from src.shared.infrastructure.query_bus.query_handlers import QueryHandlers


# --- Dummies and Mocks ---
class MyQuery(Query):
    pass

class AnotherQuery(Query):
    pass

class MyResponse(Response):
    pass

class MyQueryHandler(QueryHandler[MyQuery, MyResponse]):
    def subscribed_to(self) -> type[MyQuery]:
        return MyQuery

    def handle(self, query: MyQuery) -> MyResponse:
        return MyResponse()

class AnotherQueryHandler(QueryHandler[AnotherQuery, MyResponse]):
    def subscribed_to(self) -> type[AnotherQuery]:
        return AnotherQuery

    def handle(self, query: AnotherQuery) -> MyResponse:
        return MyResponse()


# --- Test Class ---
class TestQueryHandlers:

    def test_initialization_registers_handlers_correctly(self):
        handler1 = MyQueryHandler()
        handler2 = AnotherQueryHandler()
        
        query_handlers_instance = QueryHandlers([handler1, handler2])

        retrieved_handler1 = query_handlers_instance.get(MyQuery())
        retrieved_handler2 = query_handlers_instance.get(AnotherQuery())

        assert retrieved_handler1 is handler1
        assert retrieved_handler2 is handler2

    def test_initialization_with_empty_list(self):
        query_handlers_instance = QueryHandlers([])

        with pytest.raises(QueryNotRegisteredError):
            query_handlers_instance.get(MyQuery())

    def test_get_returns_correct_handler(self):
        handler = MyQueryHandler()
        query_handlers_instance = QueryHandlers([handler])

        retrieved_handler = query_handlers_instance.get(MyQuery())

        assert retrieved_handler is handler

    def test_get_raises_error_for_unregistered_query(self):
        query_handlers_instance = QueryHandlers([])

        with pytest.raises(QueryNotRegisteredError) as excinfo:
            query_handlers_instance.get(MyQuery())

        assert f"The query <MyQuery> hasn't a query handler associated" in str(excinfo.value)