from typing import List, Optional

from sqlmodel import select

from src.core.decorators import with_session
from src.models.note import Note, NoteType


class NoteRepository:
    """
    Manages CRUD operations for notes in a TinyDB database.

    Attributes:
        db_path (Path): The path to the TinyDB JSON file.
        db (TinyDB): The TinyDB instance.
        notes_table (Table): The TinyDB table instance for notes.
    """

    @with_session
    def get_all_notes(self, session) -> List[Note]:
        return session.exec(select(Note)).all()

    @with_session
    def get_note_by_id(self, session, note_id) -> Note:
        return session.get(Note, note_id)

    @with_session
    def add_note(
        self, session, title: str, note_type: NoteType = NoteType.PERSONAL
    ) -> Note:
        note = Note(title=title, note_type=note_type)
        session.add(note)
        session.commit()
        session.refresh(note)
        return note

    @with_session
    def update_note(self, session, note_id: int, updates: dict) -> bool:
        if not (note := session.get(Note, note_id)):
            return False

        for key, value in updates.items():
            setattr(note, key, value)
        session.commit()
        return True

    @with_session
    def delete_note(self, session, note_id: int) -> bool:
        if not (note := session.get(Note, note_id)):
            return False

        session.delete(note)
        session.commit()
        return True

    @with_session
    def filter_notes(
        self,
        session,
        note_type: Optional[NoteType] = None,
        completed: Optional[bool] = None,
    ) -> List[Note]:
        query = select(Note)

        if note_type:
            query = query.where(Note.note_type == note_type)
        if completed is not None:
            if completed:
                query = query.where(Note.completed_at is not None)
            else:
                query = query.where(Note.completed_at is None)

        return session.exec(query).all()
