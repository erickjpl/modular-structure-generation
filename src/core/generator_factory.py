import importlib
import pkgutil
from pathlib import Path

from core.interfaces.base_class import BaseGenerator, LanguagePlugin


class GeneratorFactory:
  def __init__(self):
    self._plugins: dict[str, LanguagePlugin] = {}
    self._load_plugins()

  def _load_plugins(self):
    plugins_dir = Path(__file__).parent.parent / "plugins"
    for _finder, name, _ in pkgutil.iter_modules([str(plugins_dir)]):
      module = importlib.import_module(f"plugins.{name}")
      for item in dir(module):
        obj = getattr(module, item)
        try:
          if issubclass(obj, LanguagePlugin) and obj is not LanguagePlugin:
            plugin = obj()
            self._plugins[plugin.language_name.lower()] = plugin
        except TypeError:
          continue

  def get_generator(self, language: str, framework: str | None = None) -> BaseGenerator:
    language = language.lower()
    if language not in self._plugins:
      raise ValueError(f"Unsupported language: {language}")

    return self._plugins[language].get_generator(framework)
