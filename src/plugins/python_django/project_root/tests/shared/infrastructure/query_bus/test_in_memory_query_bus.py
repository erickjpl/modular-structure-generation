from unittest.mock import MagicMock

import pytest

from src.shared.domain.queries.query import Query
from src.shared.domain.queries.query_handler import QueryHandler
from src.shared.domain.queries.query_not_registered_error import QueryNotRegisteredError
from src.shared.domain.queries.response import Response
from src.shared.infrastructure.query_bus.query_handlers import QueryHandlers
from src.shared.infrastructure.query_bus.in_memory_query_bus import InMemoryQueryBus


# --- Dummies and Mocks ---
class MyQuery(Query):
    pass

class MyResponse(Response):
    pass

class MyQueryHandler(QueryHandler[MyQuery, MyResponse]):
    def subscribed_to(self) -> type[MyQuery]:
        return MyQuery

    def handle(self, query: MyQuery) -> MyResponse:
        return MyResponse()


# --- Test Class ---
class TestInMemoryQueryBus:

    @pytest.fixture
    def query_handler(self):
        return MagicMock(spec=MyQueryHandler)

    @pytest.fixture
    def query_handlers_info(self, query_handler):
        # Mock QueryHandlers to return our specific handler
        mock_query_handlers = MagicMock(spec=QueryHandlers)
        mock_query_handlers.get.return_value = query_handler
        return mock_query_handlers

    @pytest.fixture
    def query_bus(self, query_handlers_info):
        return InMemoryQueryBus(query_handlers_info)

    def test_ask_calls_correct_handler_and_returns_response(self, query_bus, query_handler):
        # Arrange
        query = MyQuery()
        expected_response = MyResponse()
        query_handler.handle.return_value = expected_response

        # Act
        response = query_bus.ask(query)

        # Assert
        query_handler.handle.assert_called_once_with(query)
        assert response is expected_response

    def test_ask_raises_error_if_query_not_registered(self, query_bus, query_handlers_info):
        # Arrange
        query = MyQuery()
        query_handlers_info.get.return_value = None # Simulate query not registered

        # Act & Assert
        with pytest.raises(QueryNotRegisteredError) as excinfo:
            query_bus.ask(query)

        assert f"The query <MyQuery> hasn't a query handler associated" in str(excinfo.value)
