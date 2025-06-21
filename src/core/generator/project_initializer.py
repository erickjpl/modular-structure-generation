import subprocess
from pathlib import Path
from shutil import copytree

from core.interfaces.init_command_base import InitCommandConfig
from core.services.template_manager import TemplateManager


class ProjectInitializer:
  def __init__(self):
    self.template_manager = TemplateManager()

  def initialize_project(self, config: InitCommandConfig):
    self._create_project_structure(config)
    self._process_template_files(config)

    if not config.not_git:
      self._initialize_git_repo(config.path)

    if config.use_docker:
      self._setup_docker(config)

  def _create_project_structure(self, config: InitCommandConfig):
    config.path.mkdir(parents=True, exist_ok=True)

  def _process_template_files(self, config: InitCommandConfig):
    template_path = self.template_manager.get_template_path(config.template)
    copytree(template_path, config.path, dirs_exist_ok=True)

    self._replace_template_vars(
      config.path, {"PROJECT_NAME": config.name_project or config.path.name, "DATABASE": config.database.value}
    )

  def _replace_template_vars(self, path: Path, variables: dict[str, str]):
    for file in path.rglob("*"):
      if file.is_file():
        content = file.read_text()
        for key, value in variables.items():
          content = content.replace(f"{{{{ {key} }}}}", value)
        file.write_text(content)

  def _initialize_git_repo(self, path: Path):
    try:
      subprocess.run(["git", "init", str(path)], check=True)
    except subprocess.CalledProcessError:
      print("⚠️  Git initialization failed (git may not be installed)")

  def _setup_docker(self, config: InitCommandConfig):
    docker_files = self.template_manager.get_docker_files(config.template)

    for src, dest in docker_files.items():
      (config.path / dest).write_text(src.read_text())
