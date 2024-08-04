import os
from typing import Optional, Set, List
from .box import (
    FoxBox,
    MemBox,
    LogBox,
    StorageBox,

    BoxManager,
)
from .database import Schema
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

    Parameters
    ----------
    path: str = None
        database path

    schema: Schema = Schema
        define table columns structure

    box: List[FoxBox] = BASIC_BOX
        determine operations endpoint operate stage

    auto_setup: bool = True
        auto create and load database, db will create if db not exists

    auto_enable: bool = True
        for manage box activity
    """

    def __init__(self,
                 path: str = None,
                 schema: Schema = Schema,
                 box: Optional[Set[FoxBox]] = None,
                 auto_setup: bool = True,
                 auto_enable: bool = True
                 ):
        self.path = path
        self.schema: Schema = schema
        self._db = self.schema
        if box is None:
            box = BASIS_BOX

        if auto_setup:
            self.session.auto_setup()

        super(FoxLin, self).__init__(*box, auto_enable=auto_enable)

    @property
    def session(self) -> FoxSession:
        return self.establish_session(FoxSession, {1, 2})

    def _commiter(self, commit_list: List[CRUDOperation]):
        """
        this is a bridge between sessions and box manager to send the operation to get perform
        work when session.commit() called
        """
        list(map(self.operate, commit_list))
        self.operate(DBDump(db=self._db, path=self.path))
        # apply change of database from memory to file-based db
