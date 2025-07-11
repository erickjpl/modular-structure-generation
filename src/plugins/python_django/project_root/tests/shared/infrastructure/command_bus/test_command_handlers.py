from unittest.mock import MagicMock

import pytest

from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_handler import CommandHandler
from src.shared.domain.commands.command_not_registered_error import CommandNotRegisteredError
from src.shared.infrastructure.command_bus.command_handlers import CommandHandlers


# --- Dummies and Mocks ---
class DummyCommand(Command):
    pass

class AnotherDummyCommand(Command):
    pass

class DummyCommandHandler(CommandHandler[DummyCommand]):
    def __init__(self, service: MagicMock = None):
        super().__init__(service if service else MagicMock())

    def subscribed_to(self) -> type[DummyCommand]:
        return DummyCommand

    def handle(self, command: DummyCommand) -> None:
        pass

class AnotherDummyCommandHandler(CommandHandler[AnotherDummyCommand]):
    def __init__(self, service: MagicMock = None):
        super().__init__(service if service else MagicMock())

    def subscribed_to(self) -> type[AnotherDummyCommand]:
        return AnotherDummyCommand

    def handle(self, command: AnotherDummyCommand) -> None:
        pass


# --- Test Class ---
class TestCommandHandlers:

    def test_initialization_registers_handlers_correctly(self):
        handler1 = DummyCommandHandler()
        handler2 = AnotherDummyCommandHandler()
        
        command_handlers_instance = CommandHandlers([handler1, handler2])

        retrieved_handler1 = command_handlers_instance.get(DummyCommand())
        retrieved_handler2 = command_handlers_instance.get(AnotherDummyCommand())

        assert retrieved_handler1 is handler1
        assert retrieved_handler2 is handler2

    def test_initialization_with_empty_list(self):
        command_handlers_instance = CommandHandlers([])

        with pytest.raises(CommandNotRegisteredError):
            command_handlers_instance.get(DummyCommand())

    def test_get_returns_correct_handler(self):
        handler = DummyCommandHandler()
        command_handlers_instance = CommandHandlers([handler])

        retrieved_handler = command_handlers_instance.get(DummyCommand())

        assert retrieved_handler is handler

    def test_get_raises_error_for_unregistered_command(self):
        command_handlers_instance = CommandHandlers([])

        with pytest.raises(CommandNotRegisteredError) as excinfo:
            command_handlers_instance.get(DummyCommand())

        assert f"The command <DummyCommand> hasn't a command handler associated" in str(excinfo.value)