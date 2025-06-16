from functools import wraps
from typing import Callable
from src.core.database import db


def with_session(func: Callable) -> Callable:
    """
    Usage:
        @with_session
        def some_method(self, session, ...):
            return session.exec(...)
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with db.get_session() as session:
            return func(self, session, *args, **kwargs)

    return wrapper
