from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field


class NoteType(str, Enum):
    PROJECT = "project"
    INFRA = "infra"
    PERSONAL = "personal"


class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    note_type: NoteType = NoteType.PERSONAL
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    @property
    def status_display(self) -> str:
        return "✅ Completed" if self.is_completed else "⏳ Pending"

    @property
    def created_display(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M")
