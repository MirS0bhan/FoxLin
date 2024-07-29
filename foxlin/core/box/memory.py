from .base import FoxBox

from foxlin.core.query import FoxQuery
from foxlin.core.operation.crud import(
    DBCreate,
    DBRead,
    DBUpdate,
    DBDelete
)

from foxlin.core.operation.base import Log

class MemBox(FoxBox):
    level: str = 'memory'

    # def create_op(self, obj: DBCreate):
    #     return self.create_opv1(obj)
    #     db = obj.db
    #     columns = obj.create # except ID column

    #     def insert(record):
    #         flag = db.ID.plus()
    #         tuple(map(lambda col: db[col].__setitem__(flag, record[col]), columns))

    #     tuple(map(insert, obj.record))

    def create_op(self, obj: DBCreate):
        db = obj.db
        columns = obj.create

        for col in columns:
            print(col)
            cold = [r[col] for r in obj.record]
            print(cold)
            db[col].attach(cold)
            
        print(db['ID'].data,db['ID'].flag,len(cold))
        length = db['ID'].flag + len(cold) 
        print(length)
        db['ID'].parange(length + 1)
        print(db['ID'].data,db['ID'].flag)
        log = Log(box_level=self.level,
                      log_level='INFO',
                      message=f'database created 54564165456465at {cold}.')
        obj.logs.append(log)


    def read_op(self, obj: DBRead):
        # out of service
        q: FoxQuery = obj.session.query
        q.raw = obj.raw
        obj.record = q.SELECT(*obj.select)\
                      .ORDER_BY(obj.order)\
                      .LIMIT(obj.limit)\
                      .all()
        # TODO in 1.1

    def update_op(self, obj: DBUpdate):
        columns = obj.update
        for record in obj.record:
            _id = obj.db.ID.getv(record.ID)
            list(map(lambda col: obj.db[col].update(_id, record[col]), columns))

    def delete_op(self, obj: DBDelete):
        for rec in obj.record:
            _id = obj.db.ID.getv(rec.ID)
            list(map(lambda c:obj.db[c].pop(_id), obj.db.columns))

    __slots__ = ('_create_op','_update_op','_delete_op','_level')

