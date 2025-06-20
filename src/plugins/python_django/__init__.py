from dataclasses import dataclass

from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import FrameworkOption, LanguageOption, LanguagePlugin, LayerType
from plugins.python_django.django_application_generator import DjangoApplicationGenerator
from plugins.python_django.django_domain_generator import DjangoDomainGenerator
from plugins.python_django.django_infrastructure_generator import DjangoInfrastructureGenerator


@dataclass
class DjangoGenerators:
  domain: type[BaseGenerator]
  application: type[BaseGenerator]
  infrastructure: type[BaseGenerator]


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

  def get_generator(
    self, framework: PythonFrameworkOption | None = None, layer: LayerType | None = None
  ) -> BaseGenerator:
    if framework == PythonFrameworkOption.DJANGO:
      generators = DjangoGenerators(
        domain=DjangoDomainGenerator,
        application=DjangoApplicationGenerator,
        infrastructure=DjangoInfrastructureGenerator,
      )

      if layer == LayerType.DOMAIN:
        return generators.domain()
      elif layer == LayerType.APPLICATION:
        return generators.application()
      elif layer == LayerType.INFRASTRUCTURE:
        return generators.infrastructure()

    raise ValueError(f"Unsupported framework: {framework}")
