from enum import Enum

from core.inputs.interface_user_input import InterfaceUserInput


class CLIUserInput(InterfaceUserInput):
  def get_application_name(self) -> str:
    return input("Enter application name: ").strip()

  def get_module_name(self) -> str:
    return input("Enter module name: ").strip()

  def confirm_action(self, message: str) -> bool:
    response = input(f"{message} (y/n): ").lower().strip()
    return response == "y"

  def select_single_option(self, message: str, options: list[Enum]) -> Enum:
    print(message)
    for i, option in enumerate(options, 1):
      option_value = option.value if hasattr(option, "value") else str(option)
      print(f"{i}. {option_value}")

    while True:
      try:
        selected = int(input("Select an option (number): ").strip())
        if 1 <= selected <= len(options):
          return options[selected - 1]
        print("Invalid option, try again")
      except ValueError:
        print("Please enter a valid number")

  def select_options(self, message: str, options: list[Enum]) -> list[Enum]:
    print(message)
    for i, option in enumerate(options, 1):
      print(f"{i}. {option.value}")

    selected = input("Select options (comma separated): ").strip().split(",")
    return [options[int(s.strip()) - 1] for s in selected if s.strip().isdigit()]

  def get_entity_attributes(self) -> list[tuple[str, str]]:
    attributes = []
    while self.confirm_action("Do you want to add an attribute?"):
      name = input("Attribute name: ").strip()
      data_type = input("Attribute data type: ").strip()
      attributes.append((name, data_type))
    return attributes
