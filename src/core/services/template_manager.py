from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from core.interfaces.init_command_base import DatabaseOption, TemplateInfo, TemplateOption
from core.services.checker import DependencyManager


class TemplateManager:
  TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
  TEMPLATES_INFO = {
    TemplateOption.PYTHON_DJANGO.value: TemplateInfo(
      language="Python",
      name="Django",
      description="Django project with modern setup",
      databases=[DatabaseOption.SQLITE, DatabaseOption.POSTGRES, DatabaseOption.MYSQL],
      supports_docker=True,
      required_dependencies=[("python", "system")],
      github_url="https://github.com/django/django",
    ),
    TemplateOption.TS_EXPRESS.value: TemplateInfo(
      language="TypeScript",
      name="Express",
      description="Express.js project with TypeScript",
      databases=[DatabaseOption.SQLITE, DatabaseOption.POSTGRES, DatabaseOption.MONGODB],
      supports_docker=True,
      required_dependencies=[("node", "system"), ("npm", "system")],
      github_url="https://github.com/expressjs/express",
    ),
    TemplateOption.PHP_LARAVEL.value: TemplateInfo(
      language="PHP",
      name="Laravel",
      description="Laravel project with modern setup",
      databases=[DatabaseOption.MYSQL, DatabaseOption.POSTGRES],
      supports_docker=True,
      required_dependencies=[("php", "system"), ("composer", "system")],
      github_url="https://github.com/laravel/laravel",
    ),
  }

  def __init__(self):
    self.dependency_manager = DependencyManager()
    self.jinja_env = Environment(loader=FileSystemLoader(str(self.TEMPLATES_DIR)), autoescape=False)

  def get_template_info(self, template_name: str) -> TemplateInfo:
    if template_name not in self.TEMPLATES_INFO:
      raise ValueError(f"Template '{template_name}' not found")
    return self.TEMPLATES_INFO[template_name]

  def template_exists(self, template_name: str) -> bool:
    return template_name in self.TEMPLATES_INFO

  def validate_dependencies(self, template_name: str) -> bool:
    template_info = self.get_template_info(template_name)
    return self.dependency_manager.check_requirements(template_info.required_dependencies)

  def render_template(self, template_name: str, context: dict, output_path: Path):
    print(f"📦 Rendering template: {template_name} - {self.TEMPLATES_DIR}")
    template_path = self.TEMPLATES_DIR / template_name
    if not template_path.exists():
      raise ValueError(f"Template directory {template_name} not found")

    for item in template_path.rglob("*"):
      if item.is_file():
        relative_path = item.relative_to(template_path)
        output_file = output_path / relative_path

        if item.suffix in (".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg"):
          output_file.parent.mkdir(parents=True, exist_ok=True)
          output_file.write_bytes(item.read_bytes())
          continue

        content = self.jinja_env.from_string(item.read_text()).render(**context)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content)
