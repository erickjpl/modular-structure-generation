import re


def validate_project_name(name: str) -> str:
  if not name:
    return ""

  normalized = re.sub(r"[^\w-]", "_", name.strip().lower())

  if not re.match(r"^[a-z][a-z0-9_]*$", normalized):
    raise ValueError(
      "Project name must start with a letter and contain only lowercase letters, numbers and underscores"
    )

  return normalized
