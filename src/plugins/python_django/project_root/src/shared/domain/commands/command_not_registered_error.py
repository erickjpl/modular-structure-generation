from src.shared.domain.commands.command import Command


class CommandNotRegisteredError(Exception):
  def __init__(self, command: Command):
    super().__init__(f"The command <{command.__class__.__name__}> hasn't a command handler associated")
