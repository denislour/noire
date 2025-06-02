from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class NoteType(Enum):
    PROJECT = "PROJECT"
    INFRA = "INFRA"
    PERSONAL = "PERSONAL"


class Note(BaseModel):
    title: str
    note_type: NoteType = NoteType.PERSONAL
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    @property
    def id(self) -> int:
        return getattr(self, "_doc_id", 0)

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None

    @property
    def status_display(self) -> str:
        return "✅ Completed" if self.is_completed else "⏳ Pending"

    @property
    def created_display(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M")
