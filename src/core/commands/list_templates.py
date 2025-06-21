from core.interfaces.init_command_base import DatabaseOption, TemplateInfo


class ListTemplatesCommand:
  def __init__(self):
    self.templates = self._load_templates_info()

  def _load_templates_info(self) -> list[TemplateInfo]:
    return [
      TemplateInfo(
        language="Python",
        name="Django",
        description="Django project with modern setup",
        databases=[DatabaseOption.SQLITE.value, DatabaseOption.POSTGRES.value, DatabaseOption.MYSQL.value],
        supports_docker=True,
        required_dependencies=[("python", "system"), ("django", "python"), ("pip", "system")],
        github_url="https://github.com/django/django",
      ),
      TemplateInfo(
        language="TypeScript",
        name="Express",
        description="Express.js project with TypeScript",
        databases=[DatabaseOption.SQLITE.value, DatabaseOption.POSTGRES.value, DatabaseOption.MONGODB.value],
        supports_docker=True,
        required_dependencies=[("node", "system"), ("npm", "system"), ("typescript", "system")],
        github_url="https://github.com/expressjs/express",
      ),
      TemplateInfo(
        language="PHP",
        name="Laravel",
        description="Laravel project with modern setup",
        databases=[DatabaseOption.MYSQL.value, DatabaseOption.POSTGRES.value],
        supports_docker=True,
        required_dependencies=[("php", "system"), ("composer", "system")],
        github_url="https://github.com/laravel/laravel",
      ),
    ]

  def execute(self):
    print("Available project templates:\n")
    for template in self.templates:
      print(f"• {template.language} - {template.name}")
      print(f"  Description: {template.description}")
      print(f"  Supported databases: {', '.join(template.databases)}")
      print(f"  Docker support: {'Yes' if template.supports_docker else 'No'}\n")
