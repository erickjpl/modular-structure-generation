from implements.cli_user_iput import CLIUserInput
from orchestrator.module_generator import ModuleGenerator


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
