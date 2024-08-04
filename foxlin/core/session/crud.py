from typing import List

from foxlin.core.database import (
    Schema,
    COLUMN
)
from foxlin.core.operation import (
    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete,
)
from foxlin.core.query import FoxQuery
from .base import SessionBase, commit_recorder


class CrudSession(SessionBase):
    """
    Den is session model for FoxLin DB manager
    here Den records operations on database and over then commited,
    commit list will send to Foxlin for real operate

    oriented of SQL DML,TCL,DQL logic

    """

    @property
    def query(self):
        return FoxQuery(self)

    @commit_recorder
    def insert(self, *recs: Schema, columns: List[COLUMN] = None) -> DBCreate:
        if not columns:
            columns = self._db.columns[1:]  # except ID
        return DBCreate(record=recs, create=columns, db=self._db)

    @commit_recorder
    def read(self, **kwargs) -> DBRead:
        # out of service
        return DBRead(**kwargs, session=self)

    @commit_recorder
    def update(self, *recs: Schema, columns: List[COLUMN]) -> DBUpdate:
        return DBUpdate(record=recs, update=columns, db=self._db)

    @commit_recorder
    def delete(self, *recs: Schema) -> DBDelete:
        return DBDelete(record=recs, db=self._db)
