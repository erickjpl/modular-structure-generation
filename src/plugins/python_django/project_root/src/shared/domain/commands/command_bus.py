from abc import ABC, abstractmethod

from src.shared.domain.commands.command import Command


class CommandBus(ABC):
  @abstractmethod
  async def dispatch(self, command: Command) -> None:
    raise NotImplementedError
