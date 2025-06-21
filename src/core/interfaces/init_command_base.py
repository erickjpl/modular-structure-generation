from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class DatabaseOption(Enum):
  SQLITE = "sqlite"
  POSTGRES = "postgres"
  MYSQL = "mysql"
  MONGODB = "mongodb"


@dataclass
class TemplateInfo:
  name: str
  description: str
  databases: list[str]
  supports_docker: bool


@dataclass
class InitCommandConfig:
  template: str
  path: Path | None = None
  name_project: str | None = None
  use_docker: bool = False
  not_git: bool = False
  database: DatabaseOption = DatabaseOption.SQLITE
