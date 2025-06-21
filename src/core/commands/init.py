from argparse import SUPPRESS, ArgumentError, ArgumentParser, Namespace
from pathlib import Path

from core.generator.project_initializer import ProjectInitializer
from core.interfaces.init_command_base import DatabaseOption, InitCommandConfig, TemplateOption
from core.services.template_manager import TemplateManager
from core.services.validators import validate_project_name


class InitCommand:
  def __init__(self):
    self.template_manager = TemplateManager()
    self.parser = self._create_parser()

  def _create_parser(self) -> ArgumentParser:
    parser = ArgumentParser(
      description="Initialize a new project from a template", usage="init --template TEMPLATE [options]", add_help=False
    )

    required = parser.add_argument_group("required arguments")
    required.add_argument(
      "--template", required=True, choices=[t.value for t in TemplateOption], help="Project template to use"
    )

    optional = parser.add_argument_group("optional arguments")
    optional.add_argument("--path", type=Path, help="Project directory path")
    optional.add_argument("--name", help="Project name (will be normalized)")
    optional.add_argument(
      "--database",
      choices=[db.value for db in DatabaseOption],
      default="sqlite",
      help="Database type (default: sqlite)",
    )
    optional.add_argument("--use-docker", action="store_true", help="Include Docker setup files")
    optional.add_argument("--not-git", action="store_true", help="Skip git repository initialization")
    optional.add_argument("-h", "--help", action="help", default=SUPPRESS, help="Show this help message")

    return parser

  def _get_project_name(self, args: Namespace) -> str:
    if args.name:
      return validate_project_name(args.name)
    return validate_project_name(args.template.replace("-", "_"))

  def _get_available_templates(self) -> list[str]:
    return ["python-django", "php-laravel", "ts-express", "js-express"]

  def _get_template_choices(self) -> list[str]:
    return [f"template-{t}" for t in self.available_templates] + self.available_templates

  def _get_project_path(self, args: Namespace, project_name: str) -> Path:
    if args.path:
      return args.path / project_name
    return Path.cwd() / project_name

  def _create_config(self, args: Namespace) -> InitCommandConfig:
    project_name = self._get_project_name(args)
    project_path = self._get_project_path(args, project_name)

    return InitCommandConfig(
      template=args.template,
      path=project_path,
      name_project=project_name,
      use_docker=args.use_docker,
      not_git=args.not_git,
      database=DatabaseOption(args.database.lower()),
    )

  def execute(self, args: list[str] = None):
    try:
      parsed_args = self.parser.parse_args(args)
      config = self._create_config(parsed_args)
      self._create_config(config)

      print(f"\n🚀 Initializing project {config.name_project}")
      print(f"📦 Template: {config.template}")
      print(f"🗃️ Database: {config.database.value}")
      if config.use_docker:
        print("🐳 Docker Configuration: Yes")
      if not config.not_git:
        print(" - Git repository initialized")

      initializer = ProjectInitializer(self.template_manager)
      initializer.initialize_project(config)
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
