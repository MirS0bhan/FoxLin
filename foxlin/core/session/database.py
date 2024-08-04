from .base import SessionBase
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
    def load(self):
        # dbdo = DBLoad(
        #     callback=self.__set_db,
        #     callback_level=STORAGE,
        #     path=self.)
        #
        # dbdo.structure = self.schema
        # self.operate(dbdo)
        pass

    def create_database(self):
        # file_path = self.path
        # if os.path.exists(file_path): raise DataBaseExistsError(file_path)
        #
        # cjdbo = CreateJsonDB(path=file_path)  # cjdbo: create json database operation
        # cjdbo.structure = self.schema
        # self.operate(cjdbo)
        pass

    def auto_setup(self):
        try:
            self.create_database()
        except DataBaseExistsError:
            pass
        finally:
            # TODO set Exception for invalid Schema state
            self.load()
