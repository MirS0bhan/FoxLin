from typing import Type, NewType, Dict, Set, Optional
from pathlib import Path

from .column import IDColumn
from .utils import BaseModel, ItemBaseClass

ID = NewType('ID', int)
TABLE = NewType('TABLE', str)
BOX = NewType('BOX', str)
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

class Database:
    def __init__(self, db):
        self.db = db


class DBCarrier(BaseModel):
    db: Type[Schema] | None = None
