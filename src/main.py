from core.cli import ModuleGenerator
from core.inputs.cli_user_input import CLIUserInput


def main():
  try:
    user_input = CLIUserInput()
    generator = ModuleGenerator(user_input)
    generator.run()
    print("\nModule structure generated successfully!")
  except Exception as e:
    print(f"\nError: {str(e)}")
    exit(1)


if __name__ == "__main__":
  main()
