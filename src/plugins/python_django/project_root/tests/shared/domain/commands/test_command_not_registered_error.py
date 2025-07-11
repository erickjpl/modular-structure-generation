from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_not_registered_error import CommandNotRegisteredError


class MyTestCommand(Command):
  def __init__(self, data: str):
    self.data = data


class TestCommandNotRegisteredError:
  def test_should_create_error_with_correct_message(self):
    command = MyTestCommand("some_data")

    error = CommandNotRegisteredError(command)

    expected_message = f"The command <{MyTestCommand.__name__}> hasn't a command handler associated"
    assert str(error) == expected_message
