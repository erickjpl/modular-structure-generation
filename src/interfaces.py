from abc import ABC, abstractmethod
from enum import Enum


class IUserInput(ABC):
    @abstractmethod
    def get_application_name(self) -> str:
        pass

    @abstractmethod
    def get_module_name(self) -> str:
        pass

    @abstractmethod
    def confirm_action(self, message: str) -> bool:
        pass

    @abstractmethod
    def select_options(self, message: str, options: list[Enum]) -> list[Enum]:
        pass

    @abstractmethod
    def get_entity_attributes(self) -> list[tuple[str, str]]:
        pass


class IFileGenerator(ABC):
    @abstractmethod
    def generate(self, context: dict):
        pass
