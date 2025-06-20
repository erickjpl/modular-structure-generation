from core.generator_factory import GeneratorFactory
from core.interfaces.main import IUserInput


class ModuleGenerator:
  def __init__(self, user_input: IUserInput):
    self.factory = GeneratorFactory()
    self.user_input = user_input

  def run(self):
    context = self._collect_inputs()
    self._generate_structure(context)

  def _collect_inputs(self) -> dict:
    context = {"app_name": self.user_input.get_application_name(), "module_name": self.user_input.get_module_name()}

    languages = list(self.factory._plugins.keys())
    language = self.user_input.select_single_option("Select language:", languages)
    frameworks = self.factory._plugins[language].supported_frameworks
    framework = self.user_input.select_single_option("Select framework:", frameworks)
    context.update({"language": language, "framework": framework})

    # Resto de la recolección de inputs (igual que antes)
    # ...

    return context

  def _generate_structure(self, context: dict):
    generator = self.factory.get_generator(context["language"], context["framework"])

    if "domain_options" in context:
      generator.generate(context)

    # Generar otras capas
    # ...
