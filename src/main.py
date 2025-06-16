import typer

from src.const.commands import COMMANDS


app = typer.Typer(
    name="noir",
    help="A professional note management CLI tool",
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

for name, command_func in COMMANDS.items():
    app.command(name)(command_func)


if __name__ == "__main__":
    app()
