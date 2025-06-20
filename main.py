import abc
from enum import Enum, auto


# ==============================
# Domain Models (Enums y Clases Base)
# ==============================
class LayerType(Enum):
    DOMAIN = auto()
    APPLICATION = auto()
    INFRASTRUCTURE = auto()


class DomainOption(Enum):
    ENTITIES = "entities"
    VALUE_OBJECTS = "value_objects"
    SERVICES = "services"
    REPOSITORIES = "repositories"
    EVENTS = "events"


class ApplicationOption(Enum):
    COMMANDS = "commands"
    QUERIES = "queries"
    HANDLERS = "handlers"
    SERVICES = "services"
    DTOS = "dtos"


class CommandOption(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class QueryOption(Enum):
    LIST = "list"
    READ = "read"


class InfrastructureOption(Enum):
    PERSISTENCE = "persistence"
    API = "api"
    CONSUMERS = "consumers"
    EVENTS = "events"


class PersistenceOption(Enum):
    ENTITY_MODEL = "entity_model"
    ENTITY_REPOSITORY = "entity_repository"


class ApiOption(Enum):
    VIEWS = "views"
    SERIALIZERS = "serializers"


class ViewOption(Enum):
    LIST_VIEW = "list_view"
    CREATE_VIEW = "create_view"
    READ_VIEW = "read_view"
    UPDATE_VIEW = "update_view"
    DELETE_VIEW = "delete_view"


class SerializerOption(Enum):
    LIST_SERIALIZER = "list_serializer"
    READ_SERIALIZER = "read_serializer"


# ==============================
# Interfaces (Principio de Segregación de Interfaces)
# ==============================
class IUserInput(abc.ABC):
    @abc.abstractmethod
    def get_application_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_module_name(self) -> str:
        pass

    @abc.abstractmethod
    def confirm_action(self, message: str) -> bool:
        pass

    @abc.abstractmethod
    def select_options(self, message: str, options: list[Enum]) -> list[Enum]:
        pass

    @abc.abstractmethod
    def get_entity_attributes(self) -> list[tuple[str, str]]:
        pass


class IFileGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self, context: dict):
        pass


# ==============================
# Implementaciones Concretas
# ==============================
class CLIUserInput(IUserInput):
    def get_application_name(self) -> str:
        return input("Enter application name: ").strip()

    def get_module_name(self) -> str:
        return input("Enter module name: ").strip()

    def confirm_action(self, message: str) -> bool:
        response = input(f"{message} (y/n): ").lower().strip()
        return response == "y"

    def select_options(self, message: str, options: list[Enum]) -> list[Enum]:
        print(message)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option.value}")

        selected = input("Select options (comma separated): ").strip().split(",")
        return [options[int(s.strip()) - 1] for s in selected if s.strip().isdigit()]

    def get_entity_attributes(self) -> list[tuple[str, str]]:
        attributes = []
        while self.confirm_action("Do you want to add an attribute?"):
            name = input("Attribute name: ").strip()
            data_type = input("Attribute data type: ").strip()
            attributes.append((name, data_type))
        return attributes


class DomainLayerGenerator(IFileGenerator):
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

    def _generate_entities(
        self, module_name: str, app_name: str, attributes: list[tuple[str, str]]
    ):
        print(f"Creating entity for {module_name} with attributes: {attributes}")
        # Lógica real de generación de archivos iría aquí

    def _generate_value_objects(
        self, module_name: str, app_name: str, attributes: list[tuple[str, str]]
    ):
        print(
            f"Creating value objects for {module_name} based on attributes: {attributes}"
        )
        # Lógica real de generación de archivos iría aquí


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


# ==============================
# Orquestador (Principio de Responsabilidad Única)
# ==============================
class ModuleGenerator:
    def __init__(self, user_input: IUserInput):
        self.user_input = user_input
        self.generators = {
            LayerType.DOMAIN: DomainLayerGenerator(),
            LayerType.APPLICATION: ApplicationLayerGenerator(),
            LayerType.INFRASTRUCTURE: InfrastructureLayerGenerator(),
        }

    def run(self):
        context = self._collect_inputs()
        self._generate_structure(context)

    def _collect_inputs(self) -> dict:
        context = {
            "app_name": self.user_input.get_application_name(),
            "module_name": self.user_input.get_module_name(),
        }

        # Domain Layer
        if self.user_input.confirm_action("Do you want to configure domain layer?"):
            domain_options = self.user_input.select_options(
                "Select domain options:", list(DomainOption)
            )
            context["domain_options"] = domain_options

            if (
                DomainOption.ENTITIES in domain_options
                and self.user_input.confirm_action(
                    "Do you want to add attributes to the entity?"
                )
            ):
                context["entity_attributes"] = self.user_input.get_entity_attributes()

        # Application Layer
        if self.user_input.confirm_action(
            "Do you want to configure application layer?"
        ):
            app_options = self.user_input.select_options(
                "Select application options:", list(ApplicationOption)
            )
            context["application_options"] = app_options

            if ApplicationOption.COMMANDS in app_options:
                command_options = self.user_input.select_options(
                    "Select command types:", list(CommandOption)
                )
                context["command_options"] = command_options

            if ApplicationOption.QUERIES in app_options:
                query_options = self.user_input.select_options(
                    "Select query types:", list(QueryOption)
                )
                context["query_options"] = query_options

        # Infrastructure Layer
        if self.user_input.confirm_action(
            "Do you want to configure infrastructure layer?"
        ):
            infra_options = self.user_input.select_options(
                "Select infrastructure options:", list(InfrastructureOption)
            )
            context["infrastructure_options"] = infra_options

            if InfrastructureOption.PERSISTENCE in infra_options:
                persistence_options = self.user_input.select_options(
                    "Select persistence options:", list(PersistenceOption)
                )
                context["persistence_options"] = persistence_options

            if InfrastructureOption.API in infra_options:
                api_options = self.user_input.select_options(
                    "Select API options:", list(ApiOption)
                )
                context["api_options"] = api_options

                if ApiOption.VIEWS in api_options:
                    view_options = self.user_input.select_options(
                        "Select view types:", list(ViewOption)
                    )
                    context["view_options"] = view_options

        return context

    def _generate_structure(self, context: dict):
        # Domain Layer
        if "domain_options" in context:
            self.generators[LayerType.DOMAIN].generate(context)

        # Application Layer
        if "application_options" in context:
            self.generators[LayerType.APPLICATION].generate(context)

        # Infrastructure Layer
        if "infrastructure_options" in context:
            self.generators[LayerType.INFRASTRUCTURE].generate(context)


# ==============================
# Punto de Entrada (Principio Abierto/Cerrado)
# ==============================
def main():
    try:
        user_input = CLIUserInput()
        generator = ModuleGenerator(user_input)
        generator.run()
        print("\nModule structure generated successfully!")
    except Exception as e:
        print(f"\nError: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
