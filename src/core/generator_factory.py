import importlib
import pkgutil
from enum import Enum
from pathlib import Path

from core.interfaces.base_class import BaseGenerator, LanguagePlugin


class GeneratorFactory:
  def __init__(self):
    self._plugins: dict[str, LanguagePlugin] = {}
    self._load_plugins()

  def _load_plugins(self):
    plugins = "plugins"
    plugins_dir = Path(__file__).parent.parent / plugins

    for _, plugin_dir_name, __ in pkgutil.iter_modules([str(plugins_dir)]):
      plugin_path = plugins_dir / plugin_dir_name

      for _, module_name, __ in pkgutil.iter_modules([str(plugin_path)]):
        full_module_name = f"{plugins}.{plugin_dir_name}.{module_name}"

        try:
          module = importlib.import_module(full_module_name)

          for item_name in dir(module):
            obj = getattr(module, item_name)

            if (
              isinstance(obj, type)
              and obj is not LanguagePlugin
              and obj is not BaseGenerator
              and not issubclass(obj, type(Enum) | Enum)
            ):
              try:
                plugin = obj()
                if isinstance(plugin, LanguagePlugin):
                  self._plugins[plugin.language_name.lower()] = plugin
              except TypeError as e:
                print(f"ERROR: Could not instantiate class {obj.__name__} from module {full_module_name}: {e}")
                continue
              except Exception as e:
                print(f"ERROR: Unexpected error instantiating {obj.__name__} from module {full_module_name}: {e}")
                continue

        except ImportError as e:
          print(f"ERROR: Failed to import {full_module_name}: {e}")
          continue
        except Exception as e:
          print(f"ERROR: General error processing {full_module_name}: {e}")
          continue

  def get_generator(self, language: str, framework: str | None = None) -> BaseGenerator:
    language = language.lower()
    if language not in self._plugins:
      raise ValueError(f"Unsupported language: {language}")

    return self._plugins[language].get_generator(framework)
