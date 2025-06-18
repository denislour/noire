import typer

from src.repository.note_repository import note_repository


def delete_command(
    note_id: int = typer.Argument(..., help="The ID of the note to delete."),
) -> None:
    """Delete the note."""
    note_to_delete = note_repository.get_note_by_id(note_id)
    if not note_to_delete:
        print(f"❌ Error: Note with ID {note_id} not found.")
        raise typer.Exit(code=1)
    success = note_repository.delete_note(note_id)

    if success:
        print(f"✅ Note ID {note_id} deleted successfully.")
    else:
        print(f"❌ Error: Failed to delete note ID {note_id}.")
        raise typer.Exit(code=1)
