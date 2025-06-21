from pathlib import Path


class TemplateManager:
  TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

  def template_exists(self, template_name: str) -> bool:
    return (self.TEMPLATES_DIR / template_name).exists()

  def get_template_path(self, template_name: str) -> Path:
    return self.TEMPLATES_DIR / template_name

  def get_docker_files(self, template_name: str) -> dict[Path, str]:
    template_path = self.get_template_path(template_name)
    docker_files = {}

    dockerfile = template_path / "Dockerfile"
    if dockerfile.exists():
      docker_files[dockerfile] = "Dockerfile"

    compose_file = template_path / "docker-compose.yml"
    if compose_file.exists():
      docker_files[compose_file] = "docker-compose.yml"

    return docker_files
