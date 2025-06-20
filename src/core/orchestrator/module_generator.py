from core.generator_factory import GeneratorFactory
from core.implements.application_layer_generator import ApplicationLayerGenerator
from core.implements.domain_layer_generator import DomainLayerGenerator
from core.implements.infrastructure_layer_generator import InfrastructureLayerGenerator
from core.interfaces.base_class import (
  ApiOption,
  ApplicationOption,
  CommandOption,
  DomainOption,
  InfrastructureOption,
  LayerType,
  PersistenceOption,
  QueryOption,
  ViewOption,
)
from core.interfaces.main import IUserInput


class ModuleGenerator:
  def __init__(self, user_input: IUserInput):
    self.user_input = user_input
    self.factory = GeneratorFactory()
    self.generators = {
      LayerType.DOMAIN: DomainLayerGenerator(),
      LayerType.APPLICATION: ApplicationLayerGenerator(),
      LayerType.INFRASTRUCTURE: InfrastructureLayerGenerator(),
    }

  def run(self):
    context = self._collect_inputs()
    self._generate_structure(context)

  def _collect_inputs(self) -> dict:
    context = {"app_name": self.user_input.get_application_name(), "module_name": self.user_input.get_module_name()}

    # Selección de lenguaje y framework
    languages = list(self.factory._plugins.keys())
    language = self.user_input.select_option("Select language:", languages)
    frameworks = self.factory._plugins[language].supported_frameworks
    framework = self.user_input.select_option("Select framework:", frameworks)

    context.update({"language": language, "framework": framework})

    # Domain Layer
    if self.user_input.confirm_action("Do you want to configure domain layer?"):
      domain_options = self.user_input.select_options("Select domain options:", list(DomainOption))
      context["domain_options"] = domain_options

      if DomainOption.ENTITIES in domain_options and self.user_input.confirm_action(
        "Do you want to add attributes to the entity?"
      ):
        context["entity_attributes"] = self.user_input.get_entity_attributes()

    # Application Layer
    if self.user_input.confirm_action("Do you want to configure application layer?"):
      app_options = self.user_input.select_options("Select application options:", list(ApplicationOption))
      context["application_options"] = app_options

      if ApplicationOption.COMMANDS in app_options:
        command_options = self.user_input.select_options("Select command types:", list(CommandOption))
        context["command_options"] = command_options

      if ApplicationOption.QUERIES in app_options:
        query_options = self.user_input.select_options("Select query types:", list(QueryOption))
        context["query_options"] = query_options

    # Infrastructure Layer
    if self.user_input.confirm_action("Do you want to configure infrastructure layer?"):
      infra_options = self.user_input.select_options("Select infrastructure options:", list(InfrastructureOption))
      context["infrastructure_options"] = infra_options

      if InfrastructureOption.PERSISTENCE in infra_options:
        persistence_options = self.user_input.select_options("Select persistence options:", list(PersistenceOption))
        context["persistence_options"] = persistence_options

      if InfrastructureOption.API in infra_options:
        api_options = self.user_input.select_options("Select API options:", list(ApiOption))
        context["api_options"] = api_options

        if ApiOption.VIEWS in api_options:
          view_options = self.user_input.select_options("Select view types:", list(ViewOption))
          context["view_options"] = view_options

    return context

  def _generate_structure(self, context: dict):
    generator = self.factory.get_generator(context["language"], context["framework"])

    # Domain Layer
    if "domain_options" in context:
      generator.generate(context)
      self.generators[LayerType.DOMAIN].generate(context)

    # Application Layer
    if "application_options" in context:
      generator.generate(context)
      self.generators[LayerType.APPLICATION].generate(context)

    # Infrastructure Layer
    if "infrastructure_options" in context:
      generator.generate(context)
      self.generators[LayerType.INFRASTRUCTURE].generate(context)
