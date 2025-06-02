from typer import Typer

from commands import add_command, list_command

app = Typer(
    name="noir",
    help="A professional note management CLI tool",
    add_completion=False,
)

COMMANDS = {"add": add_command, "list": list_command}

for name, command_func in COMMANDS.items():
    app.command(name)(command_func)


if __name__ == "__main__":
    app()
