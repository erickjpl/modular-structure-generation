import subprocess
from pathlib import Path

from core.interfaces.init_command_base import InitCommandConfig
from core.services.template_manager import TemplateManager


class ProjectInitializer:
  def __init__(self):
    self.template_manager = TemplateManager()

  def initialize_project(self, config: "InitCommandConfig"):
    self._validate_project(config)
    self._create_project_structure(config)
    self._process_template_files(config)

    if not config.not_git:
      self._initialize_git_repo(config.path, config.name_project)

    if config.use_docker:
      self._setup_docker(config)

    print(f"\n🎉 Project {config.name_project} created successfully!")
    print(f"📍 Location: {config.path.absolute()}")

  def _validate_project(self, config: InitCommandConfig):
    if not self.template_manager.validate_dependencies(config.template):
      raise RuntimeError("The necessary dependencies are not met")

  def _create_project_structure(self, config: InitCommandConfig):
    config.path.mkdir(parents=True, exist_ok=True)

  def _process_template_files(self, config: "InitCommandConfig"):
    context = {"project_name": config.name_project, "database": config.database.value, "use_docker": config.use_docker}
    self.template_manager.render_template(config.template, context, config.path, config.name_project)

  def _initialize_git_repo(self, path: Path, name_project: str):
    try:
      subprocess.run(["git", "init", str(path)], check=True)
      print("\n✅ Git repository initialized")

      subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
      print("✅ All files added to staging")

      commit_message = f"Initialize project: {name_project}" if name_project else "Initialize project"
      subprocess.run(["git", "-C", str(path), "commit", "-m", commit_message], check=True)
      print(f"✅ Initial commit created: '{commit_message}'")
    except subprocess.CalledProcessError:
      print("\n⚠️  Git initialization failed (git may not be installed)")

  def _setup_docker(self, config: InitCommandConfig):
    template_info = self.template_manager.get_template_info(config.template)
    if not template_info.supports_docker:
      print("\n⚠️  Docker is not supported for this template.")
      return

    docker_context = {"project_name": config.name_project, "database": config.database.value}

    # Render Dockerfile
    dockerfile_template = f"{config.template}/Dockerfile.j2"
    dockerfile_path = config.path / "Dockerfile"
    dockerfile_content = self.template_manager.jinja_env.get_template(dockerfile_template).render(**docker_context)
    dockerfile_path.write_text(dockerfile_content)

    # Render docker-compose.yml
    compose_template = f"{config.template}/docker-compose.yml.j2"
    compose_path = config.path / "docker-compose.yml"
    compose_content = self.template_manager.jinja_env.get_template(compose_template).render(**docker_context)
    compose_path.write_text(compose_content)

    print("\n✅ Docker files configured")
