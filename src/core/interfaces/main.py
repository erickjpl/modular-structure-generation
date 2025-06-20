from abc import ABC, abstractmethod
from pathlib import Path

import jinja2


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
