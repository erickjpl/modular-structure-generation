from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class DependencyChecker(ABC):
  @abstractmethod
  def check_dependency(self, dependency: str) -> bool:
    pass

  @abstractmethod
  def install_dependency(self, dependency: str) -> bool:
    pass


class TemplateOption(Enum):
  PYTHON_DJANGO = "python-django"
  TS_EXPRESS = "ts-express"
  PHP_LARAVEL = "php-laravel"


class DatabaseOption(Enum):
  SQLITE = "sqlite"
  POSTGRES = "postgres"
  MYSQL = "mysql"
  MONGODB = "mongodb"


@dataclass
class TemplateInfo:
  language: str
  name: str
  description: str
  databases: list[str]
  supports_docker: bool
  required_dependencies: list[tuple[str, str]]
  github_url: str


@dataclass
class InitCommandConfig:
  template: str
  path: Path | None = None
  name_project: str | None = None
  use_docker: bool = False
  not_git: bool = False
  database: DatabaseOption = DatabaseOption.SQLITE
