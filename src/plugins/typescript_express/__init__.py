from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import FrameworkOption, LanguageOption, LanguagePlugin


class TypescriptFrameworkOption(FrameworkOption):
  EXPRESS = "Express"
  NEST_JS = "NestJS"


class ExpressPlugin(LanguagePlugin):
  @property
  def language_name(self) -> LanguageOption:
    return LanguageOption.TYPESCRIPT

  @property
  def supported_frameworks(self) -> list[TypescriptFrameworkOption]:
    return [TypescriptFrameworkOption.EXPRESS, TypescriptFrameworkOption.NEST_JS]

  def get_generator(self, framework: TypescriptFrameworkOption | None = None) -> BaseGenerator:
    if framework == TypescriptFrameworkOption.EXPRESS:
      pass

    if framework == TypescriptFrameworkOption.NEST_JS:
      pass

    raise ValueError(f"Unsupported framework: {framework}")
