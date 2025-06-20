from base_class import ApplicationOption, CommandOption
from interfaces import IFileGenerator


class ApplicationLayerGenerator(IFileGenerator):
    def generate(self, context: dict):
        options = context.get("application_options", [])
        module_name = context["module_name"]
        app_name = context["app_name"]
        attributes = context.get("entity_attributes", [])

        print(f"\nGenerating application layer for {app_name}.{module_name}...")

        if ApplicationOption.COMMANDS in options:
            self._generate_commands(
                module_name, app_name, context.get("command_options", []), attributes
            )

        # Implementar otros métodos para queries, handlers, etc.

    def _generate_commands(
        self,
        module_name: str,
        app_name: str,
        command_options: list[CommandOption],
        attributes: list[tuple[str, str]],
    ):
        print(f"Creating commands for {module_name}: {command_options}")
        if CommandOption.CREATE in command_options:
            print(f"Create command will use attributes: {attributes}")
        # Lógica real de generación de archivos iría aquí
