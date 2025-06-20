from core.generators import BaseGenerator
from core.plugins.python_django.django_domain_generator import DjangoDomainGenerator


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
