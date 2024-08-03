from typing import NewType

from .column import IDColumn
from .utils import BaseModel, ItemBaseClass

ID = NewType('ID', int)
COLUMN = NewType('COLUMN', str)
LEVEL = NewType('LEVEL', str)


class Schema(BaseModel, ItemBaseClass):
    """
    databaser schema aliaser & also record container
    """
    ID: IDColumn | int = IDColumn()

    @property
    def columns(self):
        return list(self.__dict__.keys())


DB_TYPE = Schema


class DBCarrier(BaseModel):
    db: DB_TYPE | None = None
