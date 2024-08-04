import os
from typing import List, Optional

from foxlin.errors import (
    DataBaseExistsError
)
from .box import (
    FoxBox,
    MemBox,
    LogBox,

    StorageBox,
    BoxManager,
)
from .database import Schema
from .operation import (
    CreateJsonDB,
    DBLoad,
    DBDump,
    CRUDOperation
)
from .session import SessionManager

BASIS_BOX = [MemBox(), StorageBox(), LogBox()]


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
                 box: Optional[List[FoxBox]] = BASIS_BOX,
                 auto_setup: bool = True,
                 auto_enable: bool = True
                 ):

        self.path = path
        self.schema: Schema = schema
        self._db = self.schema()

        super(FoxLin, self).__init__(*box, auto_enable=auto_enable)
        if auto_setup:
            self.auto_setup()

    def auto_setup(self):
        try:
            self.create_database()
        except DataBaseExistsError:
            pass
        finally:
            # TODO set Exception for invalid Schema state
            self.load()

    def load(self):
        dbdo = DBLoad(
            callback=self.__set_db,
            callback_level=StorageBox.level,
            path=self.path)

        dbdo.structure = self.schema
        self.operate(dbdo)

    def __set_db(self, op: DBLoad):
        self._db = op.db

    def create_database(self):
        file_path = self.path
        if os.path.exists(file_path): raise DataBaseExistsError(file_path)

        cjdbo = CreateJsonDB(path=file_path)  # cjdbo: create json database operation
        cjdbo.structure = self.schema
        self.operate(cjdbo)

    def _commiter(self, commit_list: List[CRUDOperation]):
        """
        this is bridge between sessions and box manager to send the operation to get perform
        work when session.commit() called
        """
        list(map(self.operate, commit_list))
        self.operate(DBDump(db=self._db, path=self.path))
        # apply change of database from memory to file-based db
