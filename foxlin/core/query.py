from operator import eq, gt, lt, contains
from random import choice
from typing import Generator, Callable, Dict, Tuple, Union, Any

from numpy import array, argsort, argwhere, arange
from typing_extensions import Self

from .column import BaseColumn
from .database import Schema
from .utils import get_attr


class BaseOpr:
    def __init__(self, op, du):
        self.op = op
        self.du = du


EQ: BaseOpr = BaseOpr(eq, '__eq__')
GT: BaseOpr = BaseOpr(gt, '__GT__')
LT: BaseOpr = BaseOpr(lt, '__lt__')
IN: BaseOpr = BaseOpr(contains, '__in__')

VAL = Any
OPR = Union[EQ, GT, LT]
CON = Tuple[OPR, VAL]


class FoxCon:
    """
    FoxCon used for saving expressions 


    Parameters
    ----------
    name: str
        column name
    column : Column
        used for data filtering
    """

    def __init__(self, name: str, column: BaseColumn):
        self.name: str = name
        self.column: BaseColumn = column
        self.uptop: CON | None = None
        self.register: Dict[OPR, VAL] = {}

    def __add(self, opr: OPR, val: VAL):
        self.register[opr] = val
        self.uptop = (opr, val)

    def __eq__(self, o):
        self.__add(EQ, o)
        return self

    def __gt__(self, o):
        self.__add(GT, o)
        return self

    def __lt__(self, o):
        self.__add(LT, o)
        return self

    def __in__(self, o):
        self.__add(IN, o)
        return self

    def filter(self):
        opr, val = self.uptop  # get last exp
        func = getattr(self.column, opr.du)  # example : return Column.__eq__
        con = func(val)

        x = argwhere(con)
        return x

    def validate(self, o):
        # will use in Query Cache system
        return any([opr.op(o, val) for opr, val in self.register.items()])

    def __getitem__(self, i):
        return self.column.data.__getitem__(i)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}:{self.register}'


class FoxQuery(object):
    """ 
    FoxQuery is an interface for operate queries on memory
    FoxQuery would get indecies of records on ID column
    and after filter them by user through where() method
    can access filtered records by all() method or first(), end(), rand()
    also can use raw param to get raw-dict data of record

    Parameters
    ----------
    session: Den
        for access to data of columns
    """

    def __init__(self, session):
        self.session = session
        self.records = []
        self.selected_col = set()
        self.raw = False

        self.reset()

    @property
    def __get_records(self):
        return arange(self.ID.column.flag)

    # manage the condition of Query

    def reset(self):
        self.records = self.__get_records
        self.selected_col = set()

    # accessing data 

    def get_by_id(self, ID: int | str) -> Schema | Dict:
        _id = self.session._db['ID'].getv(ID)
        return self.get_one(_id)

    def get_one(self, ID: int) -> Schema | Dict:
        # here ID mean index of ID in ID column
        return self.session.get_one(ID, columns=self.selected_col, raw=self.raw)

    def get_many(self, *ID: int):
        return self.session.get_many(*ID, columns=self.selected_col, raw=self.raw)

    def first(self):
        return self.get_one(self.records[0])

    def end(self):
        return self.get_one(self.records[-1])

    def rand(self):
        rand_id = choice(self.records)
        return self.get_one(rand_id)

    def all(self) -> Generator:
        return self.get_many(*self.records)

    # Queries
    def select(self, *column: str) -> Self:
        self.selected_col = set(column)
        return self

    def where(self, *condition: FoxCon) -> Self:
        recset = set(self.records)
        recs = self.__get_records

        for con in condition:
            x = recs[con.filter()]
            y = x.reshape(len(x))
            recset = recset & set(y)
        self.records = array(list(recset))
        return self

    def order_by(self, column: FoxCon) -> Self:
        recs = column[self.records]  # get filtered records column data
        sorted_recs_index = argsort(recs)  # sort them & return index's
        self.records = self.records[sorted_recs_index]  # sort ID data by sorted column data args
        return self

    # def group_by(self, *args, **kwargs) -> Self:
    #     # TODO in 1.1
    #     return self
    #
    # def having(self, *args, **kwargs) -> Self:
    #     # TODO in 1.1
    #     return self

    def limit(self, n: int) -> Self:
        self.records = self.records[:n]
        return self

    def count(self):
        # get count value of filtered records
        return len(self.records)

    def max(self, column):
        # get max value of filtered records
        return column[self.records].max()  # get max of filtered records

    def min(self, column):
        # get min value of filtered records
        return column[self.records].min()

    def mean(self, column):
        # get average value of filtered records
        return column[self.records].mean()

    def filter(self, func: Callable[[Schema], bool]) -> Self:
        """ TODO """
        f = filter(func, self.all())
        self.records = array(list(f))
        return self

    def rai(self, **exp):
        # TODO in 2.0.0
        # uses for get records by column set as a right access index type
        pass

    def __getattribute__(self, name):
        try:
            return get_attr(self, name)
        except AttributeError:  # implemented for quick access of column data like : query.<column name>
            _db = self.session._db
            assert name in _db.columns  # TODO : set exception # assert if column don't exists
            column = _db[name]  # get column
            return FoxCon(name, column)
