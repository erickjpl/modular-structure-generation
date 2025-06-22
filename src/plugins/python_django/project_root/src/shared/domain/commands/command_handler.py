from abc import ABC, abstractmethod
from typing import TypeVar

from src.shared.domain.commands.command import Command

C = TypeVar("C", bound=Command)


class CommandHandler[C: Command](ABC):
  @abstractmethod
  async def handle(self, command: C) -> None:
    raise NotImplementedError

  @classmethod
  @abstractmethod
  def subscribed_to(cls) -> type[Command]:
    raise NotImplementedError
