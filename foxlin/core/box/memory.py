from foxlin.core.operation import (
    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete,

    MEMORY,
    LEVEL
)
from .base import FoxBox


class MemBox(FoxBox):
    level: LEVEL = MEMORY

    # def create_op(self, obj: DBCreate):
    #     return self.create_opv1(obj)
    #     db = obj.db
    #     columns = obj.create # except ID column

    #     def insert(record):
    #         flag = db.ID.plus()
    #         tuple(map(lambda col: db[col].__setitem__(flag, record[col]), columns))

    #     tuple(map(insert, obj.record))

    def create_op(self, obj: DBCreate) -> None:
        # TODO: writing new
        pass

    def read_op(self, obj: DBRead):
        # out of service
        # q: FoxQuery = obj.session.query
        # q.raw = obj.raw
        # obj.record = q.SELECT(*obj.select)\
        #               .ORDER_BY(obj.order)\
        #               .LIMIT(obj.limit)\
        #               .all()
        # TODO in 1.1
        pass

    def update_op(self, obj: DBUpdate):
        # out of service 
        pass 
    
    def delete_op(self, obj: DBDelete):
        # out of service 
        pass

    __slots__ = ('_create_op', '_update_op', '_delete_op', '_level')
