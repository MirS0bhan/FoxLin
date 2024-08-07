from typing import Optional, Set, List
from .box import (
    MemBox,
    LogBox,
    StorageBox,

    BoxManager,
)
from .database import DatabaseSettings
from foxlin.core.operation import (
    DBDump,
    CRUDOperation
)

from .session import SessionManager, FoxSession
BASIS_BOX = {
    MemBox(),
    StorageBox(),
    LogBox()
}

class FoxLin(BoxManager, SessionManager):
    """
    simple, fast, funny python column based dbms
    """
    def __init__(self,
                 db: DatabaseSettings,
                 ):
        self.db = db
        super(FoxLin, self).__init__(box=db.box,db=db, auto_enable=db.auto_enable)

        if db.auto_setup:
            self.sudo.auto_setup()

    def _set_db(self, op):
        self._db = op.db

    @property
    def sudo(self) -> FoxSession:
        return self.establish_session(FoxSession, {1, 2})

    def _commiter(self, commit_list: List[CRUDOperation]):
        """
        this is a bridge between sessions and box manager to send the operation to get perform
        work when session.commit() called
        """
        list(map(self.operate, commit_list))
        self.operate(DBDump(db=self.db))
        # apply change of database from memory to file-based db
