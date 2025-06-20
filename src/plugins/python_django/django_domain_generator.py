from pathlib import Path

from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import DomainOption


class DjangoDomainGenerator(BaseGenerator):
  def __init__(self):
    template_dir = str(Path(__file__).parent / "templates")
    super().__init__(template_dir)

  def generate(self, context: dict):
    app_name = context["app_name"].lower()
    module_name = context["module_name"].lower()
    module_name_plural = context["module_name_plural"].lower()

    options = context.get("domain_options", [])
    print(f"Generating Django domain layer with options: {options}")

    if DomainOption.ENTITIES in options:
      self._generate_models(app_name, module_name_plural, module_name, context.get("entity_attributes", []))

    if DomainOption.VALUE_OBJECTS in options:
      self._generate_value_objects(app_name, module_name, context.get("entity_attributes", []))

  def _generate_models(self, app_name: str, module_name_plural: str, module_name: str, attributes: list[dict]):
    model_content = self.render_template(
      "domain/entity.py.j2",
      {
        "app_name": app_name,
        "module_name": module_name,
        "module_name_plural": module_name_plural,
        "attributes": attributes,
      },
    )

    output_path = Path(f"{app_name}/{module_name_plural}/domain/{module_name}.py")
    self.generate_file(output_path, model_content)

  def _generate_value_objects(self, context: dict):
    pass
