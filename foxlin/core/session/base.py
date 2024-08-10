import functools
import time
from contextlib import contextmanager
from typing import List, Dict, Callable, Optional, Any, Type

from foxlin.core.operation import DBOperation
from foxlin.core.utils import generate_random_name


class SessionBase:
    def __init__(self, commiter: Callable):
        self._commiter = commiter
        self._commit_list: List[DBOperation] = []
        self._commit_point: Dict[str, List] = {}

    def _add_opr(self, opr):
        self._commit_list.append(opr)
        return opr

    def commit(self, savepoint: Optional[str] = None):
        if savepoint:
            self._commiter(self._commit_point[savepoint])
            self._commit_point.pop(savepoint)
        else:
            self._commiter(self._commit_list)
        self.rollback()

    def rollback(self, savepoint: Optional[str] = None):
        self._commit_list = self._commit_point[savepoint] if savepoint else []
        if savepoint:
            self._commit_point.pop(savepoint)

    def savepoint(self, name: str):
        self._commit_point[name] = self._commit_list
        self.rollback()

    def discard(self, opr: Optional[DBOperation] = None) -> None | DBOperation:
        # remove specified operation or last operation in commit list
        if opr:
            self._commit_list.remove(opr)
        else:
            return self._commit_list.pop()
        return None


def commit_recorder(f) -> Callable:
    # put produced operations in commit list
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        opr = f(self, *args, **kwargs)
        if isinstance(opr, DBOperation):
            return self._add_opr(opr)

    return wrapper


class SessionManager:
    """Manages sessions with a pool and expiration handling."""

    def __init__(self, commiter: Any):
        self._commiter = commiter
        self._session_pool: Dict[str, Dict[str, Any]] = {}  # SessionBase pool

    def establish_session(self, Session: Type[SessionBase], privileges: set, expire_in: int = 3600) -> Type[SessionBase]:
        """
        Create and store a new session with a unique name, privileges, and expiration time.
        """
        session_name = generate_random_name()
        session_instance = dict(
            session=Session(self._commiter),
            privileges=privileges,
            expires_at=time.time() + expire_in
        )
        self._session_pool[session_name] = session_instance

        return self.get_session(session_name)

    def get_session(self, session_name: str) -> Type[SessionBase]:
        """Retrieve a session by its name."""
        session_info = self._session_pool.get(session_name)
        if session_info and session_info['expires_at'] > time.time():
            return session_info['session']
        else:
            # Remove expired session
            self._session_pool.pop(session_name, None)
            raise ValueError(f"SessionBase {session_name} does not exist or has expired.")

    @contextmanager
    def session(self, session_type: Optional[Type[SessionBase]],
                session_name: Optional[str] = None,
                privileges: set = None):
        """
        Context manager to create and handle a session.
        If session_name is provided, attempt to retrieve that session.
        If not, create a new session with optional privileges.
        """
        if session_name:
            # Try to retrieve an existing session by name
            session_instance = self.get_session(session_name)

        else:
            # Establish a new session with specified privileges or an empty set
            session_instance = self.establish_session(session_type, privileges or set())
        try:
            yield session_instance  # Yield the session instance
        finally:
            # Commit changes when exiting context
            session_instance.commit()
            # Optionally remove the session from the pool after use
            self._session_pool.pop(session_name, None)

    __slots__ = ('_session_pool', '_db', 'schema', '_commiter')
