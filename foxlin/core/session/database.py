from .base import SessionBase, commit_recorder
from foxlin.core.box.storage import STORAGE
from foxlin.errors import (
    DataBaseExistsError
)
from foxlin.core.operation import (
    CreateJsonDB,
    DBLoad,
    DBDump,
    CRUDOperation
)


class DatabaseSession(SessionBase):
    @commit_recorder
    def load(self):
        dbdo = DBLoad(
            callback="",
            callback_level=STORAGE,
            path=self.db.path)
        dbdo.structure = self.db.schema()

        return dbdo

    @commit_recorder
    def create_database(self):
        file_path = self.db.path

        cjdbo = CreateJsonDB(path=file_path)  # cjdbo: create json database operation
        cjdbo.structure = self.db.schema()
        return cjdbo

    def auto_setup(self):
        try:
            self.create_database()
        except DataBaseExistsError:
            pass
        finally:
            # TODO set Exception for invalid Schema state
            self.load()
