from src.shared.domain.commands.command import Command
from src.shared.domain.commands.command_bus import CommandBus
from src.shared.infrastructure.command_bus.command_handlers import CommandHandlers


class InMemoryCommandBus(CommandBus):
  def __init__(self, command_handlers: CommandHandlers):
    self.__command_handlers = command_handlers

  async def dispatch(self, command: Command) -> None:
    handler = self.__command_handlers.get(command)

    await handler.handle(command)
