from unittest.mock import MagicMock

import pytest

from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_handler import CommandHandler
from src.shared.domain.commands.command_not_registered_error import CommandNotRegisteredError
from src.shared.infrastructure.command_bus.command_handlers import CommandHandlers
from src.shared.infrastructure.command_bus.in_memory_command_bus import InMemoryCommandBus


# --- Dummies and Mocks ---
class MyCommand(Command):
    pass

class MyCommandHandler(CommandHandler[MyCommand]):
    def __init__(self, service: MagicMock = None):
        super().__init__(service if service else MagicMock())

    def subscribed_to(self) -> type[MyCommand]:
        return MyCommand

    def handle(self, command: MyCommand) -> None:
        pass


# --- Test Class ---
class TestInMemoryCommandBus:

    @pytest.fixture
    def command_handler(self):
        return MagicMock(spec=MyCommandHandler)

    @pytest.fixture
    def command_handlers_info(self, command_handler):
        # Mock CommandHandlers to return our specific handler
        mock_command_handlers = MagicMock(spec=CommandHandlers)
        mock_command_handlers.get.return_value = command_handler
        return mock_command_handlers

    @pytest.fixture
    def command_bus(self, command_handlers_info):
        return InMemoryCommandBus(command_handlers_info)

    def test_dispatch_calls_correct_handler(self, command_bus, command_handler):
        # Arrange
        command = MyCommand()

        # Act
        command_bus.dispatch(command)

        # Assert
        command_handler.handle.assert_called_once_with(command)

    def test_dispatch_raises_error_if_command_not_registered(self, command_bus, command_handlers_info):
        # Arrange
        command = MyCommand()
        command_handlers_info.get.return_value = None # Simulate command not registered

        # Act & Assert
        with pytest.raises(CommandNotRegisteredError) as excinfo:
            command_bus.dispatch(command)

        assert f"The command <MyCommand> hasn't a command handler associated" in str(excinfo.value)
