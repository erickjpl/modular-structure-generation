from pathlib import Path

from core.interfaces.base_class import BaseGenerator, DomainOption


class DjangoDomainGenerator(BaseGenerator):
  def __init__(self):
    template_dir = str(Path(__file__).parent / "templates")
    super().__init__(template_dir)

  def generate(self, context: dict):
    app_name = context["app_name"]
    module_name = context["module_name"]

    if DomainOption.ENTITIES in context.get("domain_options", []):
      self._generate_models(app_name, module_name, context.get("entity_attributes", []))

    if DomainOption.VALUE_OBJECTS in context.get("domain_options", []):
      self._generate_value_objects(app_name, module_name, context.get("entity_attributes", []))

  def _generate_models(self, app_name: str, module_name: str, attributes: list[dict]):
    model_content = self.render_template(
      "domain/model.py.j2", {"app_name": app_name, "module_name": module_name, "attributes": attributes}
    )

    output_path = Path(f"{app_name}/domain/{module_name}/models.py")
    self.generate_file(output_path, model_content)
