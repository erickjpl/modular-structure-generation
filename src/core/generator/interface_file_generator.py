from abc import ABC, abstractmethod


class InterfaceFileGenerator(ABC):
  @abstractmethod
  def generate(self, context: dict):
    pass
