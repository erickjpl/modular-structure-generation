from base_class import InfrastructureOption, PersistenceOption
from interfaces import IFileGenerator


class InfrastructureLayerGenerator(IFileGenerator):
    def generate(self, context: dict):
        options = context.get("infrastructure_options", [])
        module_name = context["module_name"]
        app_name = context["app_name"]

        print(f"\nGenerating infrastructure layer for {app_name}.{module_name}...")

        if InfrastructureOption.PERSISTENCE in options:
            self._generate_persistence(
                module_name, app_name, context.get("persistence_options", [])
            )

        # Implementar otros métodos para api, consumers, etc.

    def _generate_persistence(
        self,
        module_name: str,
        app_name: str,
        persistence_options: list[PersistenceOption],
    ):
        print(f"Creating persistence for {module_name}: {persistence_options}")
        # Lógica real de generación de archivos iría aquí
