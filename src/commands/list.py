from typing import Optional

from rich.console import Console
from rich.table import Table
from typer import Option

from src.models.note import NoteType
from src.databases.note_repository import NoteRepository

console = Console()


def list_command(
    note_type: Optional[NoteType] = Option(
        None, "--note-type", "-t", help="Filter by note type"
    ),
    completed: Optional[bool] = Option(None, help="Filter by completion status"),
) -> None:
    """Display list of notes with optional filtering."""
    repo = NoteRepository()
    notes = repo.filter_notes(note_type, completed)

    if not notes:
        console.print("📝 No notes found!")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=6)
    table.add_column("Title", justify="left")
    table.add_column("Type", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Created At", justify="center")

    for note in notes:
        table.add_row(
            str(note.id),
            note.title,
            note.note_type.value,
            note.status_display,
            note.created_display,
        )

    console.print(f"\n📝 Found {len(notes)} notes:")
    console.print(table)
