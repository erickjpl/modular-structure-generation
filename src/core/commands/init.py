from argparse import ArgumentError, ArgumentParser, Namespace
from pathlib import Path

from core.generator.project_initializer import ProjectInitializer
from core.interfaces.init_command_base import DatabaseOption, InitCommandConfig, TemplateOption
from core.services.validators import validate_project_name


class InitCommand:
  def __init__(self, parser: ArgumentParser | None = None):
    self.parser = parser if parser is not None else self._argument_parser()
    self._configure_parser(self.parser)

  def _argument_parser(self) -> ArgumentParser:
    return ArgumentParser(
      description="Initialize a new project from a template",
      usage="main.py init --template TEMPLATE [options]",
      add_help=False,
    )

  def _configure_parser(self, parser: ArgumentParser) -> None:
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

  def _get_project_name(self, args: Namespace) -> str:
    if args.name:
      return validate_project_name(args.name)
    return validate_project_name(args.template.replace("-", "_"))

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

  def execute(self, parsed_args: Namespace):
    try:
      config = self._create_config(parsed_args)

      print(f"\n🚀 Initializing project {config.name_project}")
      print(f"📦 Template: {config.template}")
      print(f"🗃️  Database: {config.database.value}")
      if config.use_docker:
        print("🐳 Docker Configuration: Yes")
      if not config.not_git:
        print("🥬 Setting up the Git repository: Yes")

      initializer = ProjectInitializer()
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
