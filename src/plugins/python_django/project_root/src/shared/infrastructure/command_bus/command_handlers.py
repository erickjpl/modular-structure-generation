from typing import TypeVar

from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_handler import CommandHandler
from src.shared.domain.commands.command_not_registered_error import CommandNotRegisteredError

C = TypeVar("C", bound=Command)


class CommandHandlers:
  def __init__(self, command_handlers: list[CommandHandler[Command]]):
    self.__handlers: dict[type[Command], CommandHandler[Command]] = {}

    for handler in command_handlers:
      subscribed_to_command = handler.subscribed_to()
      self.__handlers[subscribed_to_command] = handler

  def get(self, command: Command) -> CommandHandler[Command]:
    command_handler = self.__handlers.get(command.__class__)

    if not command_handler:
      raise CommandNotRegisteredError(command)

    return command_handler
