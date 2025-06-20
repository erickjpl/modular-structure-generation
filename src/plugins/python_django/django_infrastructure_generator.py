from pathlib import Path

from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import InfrastructureOption


class DjangoInfrastructureGenerator(BaseGenerator):
  def __init__(self):
    template_dir = str(Path(__file__).parent / "templates")
    super().__init__(template_dir)

  def generate(self, context: dict):
    options = context.get("infrastructure_options", [])
    print(f"Generating Django infrastructure layer with options: {options}")

    if InfrastructureOption.PERSISTENCE in options:
      self._generate_persistence(context)

    if InfrastructureOption.API in options:
      self._generate_api(context)

  def _generate_persistence(self, context: dict):
    pass

  def _generate_api(self, context: dict):
    pass
