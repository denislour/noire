from sqlmodel import SQLModel, Session, create_engine
from pathlib import Path


class DatabaseManager:
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._engine is None:
            db_path = Path("data/noir.db")
            db_path.parent.mkdir(parents=True, exist_ok=True)

        self._engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(self._engine)

    def get_session(self) -> Session:
        return Session(self._engine)


db = DatabaseManager()
