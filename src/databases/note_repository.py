from datetime import datetime
from pathlib import Path
from typing import List, Optional

from tinydb import Query, TinyDB
from src.models.note import Note, NoteType


class NoteRepository:
    """
    Manages CRUD operations for notes in a TinyDB database.

    Attributes:
        db_path (Path): The path to the TinyDB JSON file.
        db (TinyDB): The TinyDB instance.
        notes_table (Table): The TinyDB table instance for notes.
    """

    def __init__(self, db_path: str | Path = "data/notes.json"):
        """Initialize the note repository with database path."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(db_path)
        self.notes_table = self.db.table("notes")

    def _create_note_from_data(self, note_data) -> Note:
        """Create a Note object from database data."""
        note = Note.model_validate(note_data)
        note._doc_id = note_data.doc_id
        return note

    def get_all_notes(self) -> List[Note]:
        """Retrieve all notes from the database."""
        notes_data = self.notes_table.all()
        return [self._create_note_from_data(data) for data in notes_data]

    def get_notes_by_type(self, note_type: NoteType) -> List[Note]:
        """Retrieve notes filtered by note type."""
        query = Query()
        notes_data = self.notes_table.search(query.note_type == note_type.value)
        return [self._create_note_from_data(data) for data in notes_data]

    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        """Retrieve a single note by its ID."""
        note_data = self.notes_table.get(doc_id=note_id)
        if note_data is None:
            return None

        updated_note_data = self._create_note_from_data(note_data)
        return updated_note_data

    def get_notes_by_completed(self, completed: bool) -> List[Note]:
        """Retrieve notes filtered by completion status."""
        query = Query()
        condition = (
            query.completed_at is not None if completed else query.completed_at is None
        )
        notes_data = self.notes_table.search(condition)
        return [self._create_note_from_data(data) for data in notes_data]

    def filter_notes(
        self, note_type: Optional[NoteType] = None, completed: Optional[bool] = None
    ) -> List[Note]:
        """Filter notes by type and/or completion status."""
        if note_type:
            return self.get_notes_by_type(note_type)
        if completed is not None:
            return self.get_notes_by_completed(completed)
        return self.get_all_notes()

    def add_note(self, title: str, note_type: NoteType = NoteType.PERSONAL) -> Note:
        """Add a new note to the database."""
        note = Note(title=title, note_type=note_type)
        note_dict = note.model_dump(exclude={"_doc_id"}, mode="json")

        doc_id = self.notes_table.insert(note_dict)
        note._doc_id = doc_id
        return note

    def update_note(self, note_id: int, updates: dict) -> bool:
        """Update an existing note in the database."""
        if not updates:
            return False

        result = self.notes_table.update(updates, doc_ids=[note_id])
        return len(result) > 0

    def complete_note(self, note_id: int) -> bool:
        """Mark a note as completed."""
        result = self.notes_table.update(
            {"completed_at": datetime.now().isoformat()}, doc_ids=[note_id]
        )
        return len(result) > 0

    def delete_note(self, note_id: int) -> bool:
        """Delete a note from the database."""
        result = self.notes_table.remove(doc_ids=[note_id])
        return len(result) > 0
