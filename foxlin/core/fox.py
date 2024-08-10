from typing import Optional, Set, List
from .box import (
    MemBox,
    LogBox,
    StorageBox,
    FoxBox,
    BoxManager,
)
from .database import Schema
from foxlin.core.operation import (
    DBDump,
    CRUDOperation
)

from .session import SessionManager, FoxSession

from .utils import BaseModel
BASIS_BOX = {
    MemBox(),
    StorageBox(),
    LogBox()
}


class DatabaseSettings(BaseModel):
    path: str = ""
    tables: Schema
    box: Optional[Set[FoxBox]] = BASIS_BOX
    auto_setup: bool = True
    auto_enable: bool = True


class FoxLin:
    """
    simple, fast, funny python column based dbms
    """
    def __init__(self, db: DatabaseSettings):
        self.db = db
        print(self.db.box)
        self._bm = BoxManager(self.db.box)
        self._sm = SessionManager(self._commiter)

        if db.auto_setup:
            self.sudo.auto_setup()

    def _set_db(self, op):
        self._db = op.db

    @property
    def sudo(self) -> FoxSession:
        return self._sm.establish_session(FoxSession, {1, 2})

    def _commiter(self, commit_list: List[CRUDOperation]):
        """
        this is a bridge between sessions and box manager to send the operation to get perform
        work when session.commit() called
        """
        list(map(self._bm.operate, commit_list))
