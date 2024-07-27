from typing import List

from foxlin.core.utils import LEVEL
from foxlin.core.database import DBCarrier, Schema

from .base import DBOperation

class JsonDBOP(DBOperation):
    path: str
    levels: List[LEVEL] = ['storage', 'log']
    structure: Schema | None = None

    # TODO : validate path exists with pydantic validator

class CreateJsonDB(JsonDBOP):
    op_name: str = "create_database"

class DBLoad(DBCarrier, JsonDBOP):
    op_name = 'LOAD'

class DBDump(DBCarrier, JsonDBOP):
    op_name = 'DUMP'

