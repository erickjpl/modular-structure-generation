from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_bus import CommandBus
from src.shared.domain.commands.command_not_registered_error import CommandNotRegisteredError
from src.shared.infrastructure.command_bus.command_handlers import CommandHandlers


class InMemoryCommandBus(CommandBus):
  def __init__(self, command_handlers_information: CommandHandlers):
    self.__command_handlers_information = command_handlers_information

  def dispatch(self, command: Command) -> None:
    handler = self.__command_handlers_information.get(command)

    if not handler:
      raise CommandNotRegisteredError(command)

    handler.handle(command)
