from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

import jinja2


class IUserInput(ABC):
  @abstractmethod
  def get_application_name(self) -> str:
    pass

  @abstractmethod
  def get_module_name(self) -> str:
    pass

  @abstractmethod
  def confirm_action(self, message: str) -> bool:
    pass

  @abstractmethod
  def select_options(self, message: str, options: list[Enum]) -> list[Enum]:
    pass

  @abstractmethod
  def get_entity_attributes(self) -> list[tuple[str, str]]:
    pass


class IFileGenerator(ABC):
  @abstractmethod
  def generate(self, context: dict):
    pass


class BaseGenerator:
  def __init__(self, template_dir: str):
    self.template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    self.template_env = jinja2.Environment(loader=self.template_loader, trim_blocks=True, lstrip_blocks=True)

  def render_template(self, template_name: str, context: dict) -> str:
    template = self.template_env.get_template(template_name)
    return template.render(**context)

  def generate_file(self, output_path: Path, content: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
      f.write(content)

  def generate(self, context: dict):
    raise NotImplementedError
