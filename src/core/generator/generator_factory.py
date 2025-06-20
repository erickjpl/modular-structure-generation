import importlib
import pkgutil
from enum import Enum
from pathlib import Path

from core.generator.base_generator import BaseGenerator
from core.interfaces.base_class import FrameworkOption, LanguageOption, LanguagePlugin


class GeneratorFactory:
  def __init__(self):
    self._plugins: dict[LanguageOption, LanguagePlugin] = {}
    self._load_plugins()

  def _load_plugins(self):
    plugins_dir = Path(__file__).parent.parent / "plugins"
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
              self._plugins[plugin.language_name] = plugin
        except TypeError:
          continue

  def get_generator(self, language: LanguageOption, framework: FrameworkOption | None = None) -> BaseGenerator:
    if language not in self._plugins:
      raise ValueError(f"Unsupported language: {language}")

    return self._plugins[language].get_generator(framework)
