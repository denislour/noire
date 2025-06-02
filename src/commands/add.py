from typer import Option

from src.models.note import NoteType
from src.databases.note_repository import NoteRepository


def add_command(
    title: str,
    note_type: NoteType = Option(
        NoteType.PERSONAL,
        "--note-type",
        "-t",
        help="Type of note",
    ),
) -> None:
    """Add a new note to the system."""
    repo = NoteRepository()
    note = repo.add_note(title, note_type)
    print(f"✅ Added note: {note.title} (ID: {note.id}, Type: {note.note_type.value})")
