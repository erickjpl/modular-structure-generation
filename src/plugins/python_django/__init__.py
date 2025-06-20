from core.interfaces.base_class import BaseGenerator
from plugins.python_django.django_domain_generator import DjangoDomainGenerator

# from plugins.python_django.django_infrastructure_generator import DjangoInfrastructureGenerator


class DjangoPlugin:
  @property
  def language_name(self) -> str:
    return "Python"

  @property
  def supported_frameworks(self) -> list[str]:
    return ["Django"]

  def get_generator(self, framework: str | None = None) -> BaseGenerator:
    if framework == "Django":
      return DjangoDomainGenerator()

    raise ValueError(f"Unsupported framework: {framework}")
