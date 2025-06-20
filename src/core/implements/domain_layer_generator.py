from core.generator.interface_file_generator import InterfaceFileGenerator
from core.interfaces.base_class import DomainOption


class DomainLayerGenerator(InterfaceFileGenerator):
  def generate(self, context: dict):
    options = context.get("domain_options", [])
    module_name = context["module_name"]
    app_name = context["app_name"]
    attributes = context.get("entity_attributes", [])

    print(f"\nGenerating domain layer for {app_name}.{module_name}...")

    if DomainOption.ENTITIES in options:
      self._generate_entities(module_name, app_name, attributes)

    if DomainOption.VALUE_OBJECTS in options:
      self._generate_value_objects(module_name, app_name, attributes)

    # Implementar otros métodos para services, repositories, etc.

  def _generate_entities(self, module_name: str, app_name: str, attributes: list[tuple[str, str]]):
    print(f"Creating entity for {module_name} with attributes: {attributes}")
    # Lógica real de generación de archivos iría aquí

  def _generate_value_objects(self, module_name: str, app_name: str, attributes: list[tuple[str, str]]):
    print(f"Creating value objects for {module_name} based on attributes: {attributes}")
    # Lógica real de generación de archivos iría aquí
