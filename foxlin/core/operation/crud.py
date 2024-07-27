from typing import List

from .base import (
    DBOperation, 

    ID,
    COLUMN,
    LEVEL,
)



class CRUDOperation(DBOperation, DBCarrier):
    levels: List[LEVEL] = ['memory', 'log']
    record: Schema | List[Schema]


class DBCreate(CRUDOperation):
    op_name: str = 'CREATE'
    create : List[COLUMN]

class DBRead(CRUDOperation):
    op_name: str = "READ"
    session: object
    raw: bool = False

    select: List[COLUMN] | None = None
    limit: int | None = None
    where: List[tuple] | None = None
    order: str | None = None
    record: List[Schema] | None = None
    # TODO in 1.1 group & having

class DBUpdate(CRUDOperation):
    op_name: str = "UPDATE"
    update: List[COLUMN]

class DBDelete(CRUDOperation):
    op_name: str = "DELETE"