from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import FrameworkOption, LanguageOption, LanguagePlugin
from plugins.python_django.django_domain_generator import DjangoDomainGenerator

# from plugins.python_django.django_infrastructure_generator import DjangoInfrastructureGenerator


class PythonFrameworkOption(FrameworkOption):
  DJANGO = "django"
  FASTAPI = "fastapi"


class DjangoPlugin(LanguagePlugin):
  @property
  def language_name(self) -> LanguageOption:
    return LanguageOption.PYTHON

  @property
  def supported_frameworks(self) -> list[PythonFrameworkOption]:
    return [PythonFrameworkOption.DJANGO]

  def get_generator(self, framework: PythonFrameworkOption | None = None) -> BaseGenerator:
    if framework == PythonFrameworkOption.DJANGO:
      return DjangoDomainGenerator()

    raise ValueError(f"Unsupported framework: {framework}")
