from typing import Callable

from foxlin.sophy import DBOperation

class FoxBox:
    """
    Foxbox is a operate manager for CRUD and user-self operator definated
    can use in states of memory-cache database and file-based db

    dbom: database operation manager
    """
    level: str = 'set level of operation'

    def operate(self, obj: DBOperation):
        operator: Callable = getattr(self, obj.op_name.lower()+'_op')
        operator(obj)

        if obj.callback:
            if self.level == obj.callback_level:
                obj.callback(obj)

class BoxManager(FoxBox):
    def __init__(self, *box):
        self.boxbox = {bx.level: bx() for bx in box}

    def operate(self, obj):
        levels = set(obj.levels) & self.boxbox.keys()
        for level in levels:
            self.boxbox[level].operate(obj)