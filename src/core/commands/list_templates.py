from core.interfaces.init_command_base import DatabaseOption, TemplateInfo, TemplateOption


class ListTemplatesCommand:
  def __init__(self):
    self.templates = self._load_templates_info()

  def _load_templates_info(self) -> list[TemplateInfo]:
    return [
      TemplateInfo(
        name=TemplateOption.PYTHON_DJANGO,
        description="Django project with REST API support",
        databases=[DatabaseOption.SQLITE, DatabaseOption.POSTGRES, DatabaseOption.MYSQL],
        supports_docker=True,
      ),
      TemplateInfo(
        name=TemplateOption.TS_EXPRESS,
        description="Express.js project with TypeScript",
        databases=[DatabaseOption.SQLITE, DatabaseOption.POSTGRES, DatabaseOption.MYSQL, DatabaseOption.MONGODB],
        supports_docker=True,
      ),
      TemplateInfo(
        name="php-laravel",
        description="Laravel project with MVC structure",
        databases=[DatabaseOption.SQLITE, DatabaseOption.MYSQL],
        supports_docker=True,
      ),
    ]

  def execute(self):
    print("Available project templates:\n")
    for template in self.templates:
      print(f"• {template.name}")
      print(f"  Description: {template.description}")
      print(f"  Supported databases: {', '.join(template.databases)}")
      print(f"  Docker support: {'Yes' if template.supports_docker else 'No'}\n")
