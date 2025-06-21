import asyncio

from googletrans import Translator
from inflect import engine

from core.generator.generator_factory import GeneratorFactory
from core.inputs.interface_user_input import InterfaceUserInput
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


class ModuleGenerator:
  def __init__(self, user_input: InterfaceUserInput):
    self.factory = GeneratorFactory()
    self.user_input = user_input
    self.engine = engine()

  def run(self):
    context = self._collect_inputs()
    self._generate_structure(context)
    print("\n✅ Setup completed successfully\n")

  async def translate_text(self, text: str) -> str:
    async with Translator() as translator:
      try:
        result = await translator.translate(text, dest="en", src="auto")
        return result.text
      except Exception as e:
        print(f"Error trying to translate the text: {e}")
        return text

  def _collect_inputs(self) -> dict:
    context = {}

    try:
      # Friendly initial message
      print("\n🛠️  Module Generation Wizard")
      print("Press Ctrl+C at any time to cancel\n")

      # Module and Application Names Section
      print("\n📝 Module Basic Information")
      self._collect_basic_names(context)

      # Language and Framework Selection
      print("\n🌐 Language and framework selection")
      self._collect_language_and_framework(context)

      # Domain Layer
      self._collect_domain_layer_inputs(context)

      # Application Layer
      self._collect_application_layer_inputs(context)

      # Infrastructure Layer
      self._collect_infrastructure_layer_inputs(context)
    except KeyboardInterrupt:
      print("\n\n🛑 Operation canceled by user. Exiting wizard....")
      print("💡 You can run the command again whenever you need.\n")
      print("✨ Thanks for using the module builder. See you soon!")
      exit(0)
    except Exception as e:
      print(f"\n❌ Unexpected error: {str(e)}")
      print("🔧 Please report this bug so we can improve it.")
      exit(1)

    return context

  def _collect_basic_names(self, context: dict) -> None:
    app_name = self.user_input.get_application_name()
    get_module_name = self.user_input.get_module_name()
    translate_text = asyncio.run(self.translate_text(get_module_name))
    singular_noun = self.engine.singular_noun(str(translate_text))
    module_name = singular_noun if isinstance(singular_noun, str) else translate_text
    module_name_plural = self.engine.plural(module_name)
    context.update({"app_name": app_name, "module_name": module_name, "module_name_plural": module_name_plural})

  def _collect_language_and_framework(self, context: dict) -> None:
    languages = list(self.factory._plugins.keys())
    language = self.user_input.select_single_option("Select language:", languages)
    frameworks = self.factory._plugins[language].supported_frameworks
    framework = self.user_input.select_single_option("Select framework:", frameworks)
    context.update({"language": language, "framework": framework})

  def _collect_domain_layer_inputs(self, context: dict) -> None:
    if self.user_input.confirm_action("Do you want to configure domain layer?"):
      print("\n🏗️  Domain layer configuration")
      domain_options = self.user_input.select_options("Select domain options:", list(DomainOption))
      context.update({"domain_options": domain_options})

      if DomainOption.ENTITIES in domain_options and self.user_input.confirm_action(
        "Do you want to add attributes to the entity?"
      ):
        context.update({"entity_attributes": self.user_input.get_entity_attributes()})

  def _collect_application_layer_inputs(self, context: dict) -> None:
    if self.user_input.confirm_action("Do you want to configure application layer?"):
      print("\n🏗️  Application layer configuration")
      app_options = self.user_input.select_options("Select application options:", list(ApplicationOption))
      context["application_options"] = app_options

      if ApplicationOption.COMMANDS in app_options:
        command_options = self.user_input.select_options("Select command types:", list(CommandOption))
        context["command_options"] = command_options

      if ApplicationOption.QUERIES in app_options:
        query_options = self.user_input.select_options("Select query types:", list(QueryOption))
        context["query_options"] = query_options

  def _collect_infrastructure_layer_inputs(self, context: dict):
    if self.user_input.confirm_action("Do you want to configure infrastructure layer?"):
      print("\n🏗️  Infrastructure layer configuration")
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

  def _generate_structure(self, context: dict):
    self._generate_domain_layer(context)
    self._generate_application_layer(context)
    self._generate_infrastructure_layer(context)

  def _generate_domain_layer(self, context: dict):
    if "domain_options" in context:
      print("INFO: Generating Domain Layer...")
      domain_generator = self.factory.get_generator(context["language"], context["framework"], LayerType.DOMAIN)
      domain_generator.generate(context)

  def _generate_application_layer(self, context: dict):
    if "application_options" in context:
      print("INFO: Generating Application Layer...")
      application_generator = self.factory.get_generator(
        context["language"], context["framework"], LayerType.APPLICATION
      )
      application_generator.generate(context)

  def _generate_infrastructure_layer(self, context: dict):
    if "infrastructure_options" in context:
      print("INFO: Generating Infrastructure Layer...")
      infrastructure_generator = self.factory.get_generator(
        context["language"], context["framework"], LayerType.INFRASTRUCTURE
      )
      infrastructure_generator.generate(context)
