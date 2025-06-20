from pathlib import Path

from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import ApplicationOption


class DjangoApplicationGenerator(BaseGenerator):
  def __init__(self):
    template_dir = str(Path(__file__).parent / "templates")
    super().__init__(template_dir)

  def generate(self, context: dict):
    options = context.get("application_options", [])
    print(f"Generating Django application layer with options: {options}")

    if ApplicationOption.COMMANDS in options:
      self._generate_commands(context)

    if ApplicationOption.QUERIES in options:
      self._generate_value_objects(context)

  def _generate_commands(self, context: dict):
    pass

  def _generate_queries(self, context: dict):
    pass
