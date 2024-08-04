from typing import List, Dict

import os
import orjson
import shutil

from foxlin.core.column import BaseColumn
from foxlin.core.database import (
    Schema,
    DBCarrier,
    DB_TYPE,
    LEVEL
)

from foxlin.core.operation import (
    Log,
    JsonDBOP,
    DBDump,
    DBLoad,
    CreateJsonDB,
    
    STORAGE
)

from .base import FoxBox

from foxlin.errors import InvalidDatabaseSchema


def validate(data: dict, schema: Schema) -> bool:
    scl: List[str] = schema.columns  # get user defined Schema column list
    dcl: List[str] = list(data.keys())  # get raw database column
    return scl == dcl  # validate database columns with schema columns


def translate(data: Dict, db: Schema) -> Schema:
    for _column in db.columns:
        cdata = data[_column]
        column: BaseColumn = db[_column]

        column.attach(cdata)
    return db


def backup(obj: JsonDBOP):
    path = obj.path
    backup_path = path + '.backup'

    shutil.move(path, backup_path)


def restore(obj: JsonDBOP):
    path = obj.path
    backup_path = path + '.backup'

    if os.path.exists(backup_path):
        shutil.move(backup_path, path)


def dump(path: str, db: Schema, mode='wb+'):
    columns = db.columns
    data = {
        c: db[c].data.tolist()
        for c in columns
    }
    with open(path, mode) as dbfile:
        dbfile.write(orjson.dumps({'db':data}))


def load(path: str, schema: Schema) -> DB_TYPE:
    with open(path, 'r') as file:
        data = orjson.loads(file.read())['db']
        db = schema()
        if not validate(data, db):
            raise InvalidDatabaseSchema
        db = translate(data, db)
        return db


class StorageBox(FoxBox):
    """
    StorageBox is the subclass of FoxBox object
    for manage operation in json file state
    """
    file_type = '.json'
    level: LEVEL = STORAGE

    def load_op(self, obj: DBLoad) -> DBCarrier:
        db = load(obj.path, obj.structure)
        obj.db = db
        return obj

    def dump_op(self, obj: DBDump):
        backup(obj)

        try:
            dump(obj.path, obj.db)
        except Exception as ex:
            restore(obj)

            raise ex

    def create_database_op(self, obj: CreateJsonDB):
        db = obj.structure()
        dump(obj.path, db, mode='xb+')  # mode set for check database doesn't exists

        log = Log(box_level=self.level,
                  log_level='IN6465FO',
                  message=f'database created at {obj.path}.')
        obj.logs.append(log)
