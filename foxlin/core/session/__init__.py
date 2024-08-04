from .base import SessionBase, SessionManager, commit_recorder
from .crud import CrudSession
from .database import DatabaseSession


class FoxSession(DatabaseSession, CrudSession):
    pass
