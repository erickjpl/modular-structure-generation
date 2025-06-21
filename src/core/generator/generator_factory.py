import importlib
import pkgutil
from enum import Enum
from pathlib import Path

from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import FrameworkOption, LanguageOption, LanguagePlugin, LayerType


class GeneratorFactory:
  def __init__(self):
    self._plugins: dict[LanguageOption, LanguagePlugin] = {}
    self._load_plugins()

  def _load_plugins(self):
    plugins_dir = Path(__file__).parent.parent.parent / "plugins"
    for _finder, name, _ in pkgutil.iter_modules([str(plugins_dir)]):
      module = importlib.import_module(f"plugins.{name}")
      for item in dir(module):
        obj = getattr(module, item)
        try:
          if (
            isinstance(obj, type)
            and obj is not LanguagePlugin
            and obj is not BaseGenerator
            and not issubclass(obj, type(Enum) | Enum)
          ):
            plugin = obj()

            if isinstance(plugin, LanguagePlugin):
              print(f"INFO: Loading plugin: {plugin.language_name}")
              self._plugins[plugin.language_name] = plugin
        except TypeError:
          continue

  def get_generator(
    self, language: LanguageOption, framework: FrameworkOption | None = None, layer: LayerType | None = None
  ) -> BaseGenerator:
    if language not in self._plugins:
      raise ValueError(
        f"Unsupported language '{language.value}' is not supported."
        f"Available options: {[lang.value for lang in self._plugins]}"
      )

    plugin = self._plugins[language]

    if framework is not None and framework not in plugin.supported_frameworks:
      raise ValueError(
        f"Framework '{framework.value}' is not supported for language '{language.value}'. "
        f"Available options: {[f.value for f in plugin.supported_frameworks]}"
      )

    generator = plugin.get_generator(framework, layer)

    if layer is not None and not self._validate_layer_support(generator, layer):
      supported_layers = self._get_supported_layers(generator)
      raise ValueError(
        f"Layer '{layer.value}' is not supported by this generator. "
        f"Available layers: {[layer.value for layer in supported_layers]}"
      )

    return self._plugins[language].get_generator(framework)

  def _validate_layer_support(self, generator: BaseGenerator, layer: LayerType) -> bool:
    layer_methods = {
      LayerType.DOMAIN: hasattr(generator, "generate_domain"),
      LayerType.APPLICATION: hasattr(generator, "generate_application"),
      LayerType.INFRASTRUCTURE: hasattr(generator, "generate_infrastructure"),
    }
    return layer_methods.get(layer, False)

  def _get_supported_layers(self, generator: BaseGenerator) -> list[LayerType]:
    supported = []
    if hasattr(generator, "generate_domain"):
      supported.append(LayerType.DOMAIN)
    if hasattr(generator, "generate_application"):
      supported.append(LayerType.APPLICATION)
    if hasattr(generator, "generate_infrastructure"):
      supported.append(LayerType.INFRASTRUCTURE)
    return supported
