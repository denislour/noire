# src/commands/update.py
from typing import Optional
import typer
from src.databases.note_repository import NoteRepository
from src.models.note import NoteType


def update_command(
    note_id: int = typer.Argument(..., help="The ID of the note to update."),
    new_title: Optional[str] = typer.Option(
        None,
        "--title",
        "-t",
        help="The new title for the note.",
        show_default=False,
    ),
    new_note_type: Optional[NoteType] = typer.Option(
        None,
        "--note-type",
        "-nt",
        help="The new type for the note (e.g., PERSONAL, PROJECT, INFRA).",
        case_sensitive=False,
        show_default=False,
    ),
) -> None:
    """Update the title and/or type of an existing note."""
    repo = NoteRepository()
    note_to_update = repo.get_note_by_id(note_id)

    if not note_to_update:
        print(f"❌ Error: Note with ID {note_id} not found.")
        raise typer.Exit(code=1)

    fields_to_update = {}

    if new_title is not None and note_to_update.title != new_title:
        fields_to_update["title"] = new_title

    if new_note_type is not None and note_to_update.note_type != new_note_type:
        fields_to_update["note_type"] = new_note_type.value

    if not fields_to_update:
        print(
            f"ℹ️ No new information provided or values are identical to the current ones for note ID {note_id}. No update performed."
        )
        return

    success = repo.update_note(note_id, fields_to_update)

    if success:
        print(f"✅ Note ID {note_id} updated successfully.")
    else:
        print(f"❌ Error: Failed to update note ID {note_id}.")
        raise typer.Exit(code=1)
