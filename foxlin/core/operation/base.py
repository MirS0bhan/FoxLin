from typing import List, Callable
from ..utils import BaseModel, LEVEL


class Log(BaseModel):
    box_level: str
    log_level: str
    message: object = None

class DBOperation(BaseModel):
    """
    for manage operation in the different data management level of program,
    we use DBOperation to transfer operation between levels
    """
    op_name: str
    callback: Callable | None = None
    callback_level: LEVEL | None= None  # that level callback can call

    levels: List[LEVEL] = ['log']
    logs: List[Log] = []
