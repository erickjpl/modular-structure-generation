from argparse import SUPPRESS, ArgumentError, ArgumentParser, Namespace
from pathlib import Path

from core.generator.project_initializer import ProjectInitializer
from core.interfaces.init_command_base import DatabaseOption, InitCommandConfig
from core.services.template_manager import TemplateManager
from core.services.validators import validate_project_name


class InitCommand:
  def __init__(self):
    self.parser = self._create_parser()
    self.available_templates = self._get_available_templates()
    self.template_manager = TemplateManager()
    self.initializer = ProjectInitializer()

  def _create_parser(self) -> ArgumentParser:
    parser = ArgumentParser(
      description="Initialize a new project from a template",
      usage="cli init --template-<name> [options]",
      add_help=False,
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
      "--template",
      required=True,
      choices=self._get_template_choices(),
      help="Project template to use (e.g. python-django, php-laravel)",
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument("--path", type=Path, help="Project directory path (default: ./<project-name>)")
    optional.add_argument("--name-project", help="Project name (will be normalized)")
    optional.add_argument(
      "--database",
      choices=[db.value for db in DatabaseOption],
      default="sqlite",
      help="Database type (default: sqlite)",
    )
    optional.add_argument("--use-docker", action="store_true", help="Include Docker setup files")
    optional.add_argument("--not-git", action="store_true", help="Skip git repository initialization")
    optional.add_argument("-h", "--help", action="help", default=SUPPRESS, help="Show this help message and exit")

    return parser

  def _get_available_templates(self) -> list[str]:
    return ["python-django", "php-laravel", "ts-express", "js-express"]

  def _get_template_choices(self) -> list[str]:
    return [f"template-{t}" for t in self.available_templates] + self.available_templates

  def execute(self, args: list[str] = None):
    try:
      parsed_args = self.parser.parse_args(args)
      config = self._create_config(parsed_args)
      self._validate_config(config)

      print(f"🚀 Initializing project with template: {config.template}")
      self.initializer.initialize_project(config)

      print(f"\n✅ Project initialized successfully at {config.path}")
      if not config.not_git:
        print("  - Git repository initialized")
      if config.use_docker:
        print(f"  - Docker files created for {config.database.value}")
      print(f"  - Template used: {config.template}")
    except ArgumentError as e:
      print(f"\n❌ Argument error: {str(e)}")
      self.parser.print_help()
      exit(1)
    except ValueError as e:
      print(f"\n❌ Validation error: {str(e)}")
      exit(1)
    except Exception as e:
      print(f"\n❌ Unexpected error: {str(e)}")
      exit(1)

  def _create_config(self, args: Namespace) -> InitCommandConfig:
    name_project = validate_project_name(args.name_project) if args.name_project else None

    base_name = name_project or args.template.replace("template-", "").replace("-", "_")

    project_path = args.path / base_name if args.path else Path.cwd() / base_name

    return InitCommandConfig(
      template=args.template,
      path=project_path,
      name_project=name_project,
      use_docker=args.use_docker,
      not_git=args.not_git,
      database=DatabaseOption(args.database.lower()),
    )

  def _validate_config(self, config: InitCommandConfig):
    if not self.template_manager.template_exists(config.template):
      raise ValueError(f"Template '{config.template}' not found")

    if config.path.exists():
      raise ValueError(f"Path '{config.path}' already exists")

    if not self.template_manager.template_exists(config.template):
      available = ", ".join(self.available_templates)
      raise ValueError(f"Template '{config.template}' not found. Available templates: {available}")

    if config.path.exists():
      raise ValueError(f"Directory '{config.path}' already exists. Please choose a different path or name.")
