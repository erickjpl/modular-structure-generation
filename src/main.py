from argparse import ArgumentParser

from core.cli import ModuleGenerator
from core.commands.init import InitCommand
from core.commands.list_templates import ListTemplatesCommand
from core.inputs.cli_user_input import CLIUserInput


def main():
  parser = ArgumentParser(description="CLI Tool for project scaffolding and module generation")
  subparsers = parser.add_subparsers(dest="command", required=True)
  init_parser = subparsers.add_parser("init", help="Initialize a new project from template")
  subparsers.add_parser("list-templates", help="List all available project templates")
  subparsers.add_parser("generate", help="Generate module structure")

  init_cmd = InitCommand(init_parser)

  args = parser.parse_args()

  try:
    if args.command == "init":
      init_cmd.execute(args)
    elif args.command == "list-templates":
      list_templates_cmd = ListTemplatesCommand()
      list_templates_cmd.execute()
    elif args.command == "generate":
      user_input = CLIUserInput()
      generator = ModuleGenerator(user_input)
      generator.run()
      print("\n✅ Module structure generated successfully!")
  except Exception as e:
    print(f"\nError: {str(e)}")
    exit(1)


if __name__ == "__main__":
  main()
