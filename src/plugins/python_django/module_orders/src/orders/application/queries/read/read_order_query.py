from dataclasses import dataclass


@dataclass(frozen=True)
class ReadOrderQuery:
  pk: str = None
