class Den(object):
    """
    Den is session model for FoxLin DB manager
    here Den records operations on database and over then commited, commit list will send to Foxlin for real operate
    and session will be delete.
    """
    def __init__(self,
                 db: DBCarrier,
                 schema: Schema,
                 commiter: Callable
            ):
        self.__db: DB_TYPE = db
        self._schema: Schema = schema
        self._commiter = commiter


        self._commit_list: List[CRUDOperation] = []


    @staticmethod
    def _commitRecorder(f) -> Callable:
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            r = f(self,*args,**kwargs)
            if isinstance(r,CRUDOperation):
                self._commit_list.append(r)
        return wrapper

    def select(self,ID: int) -> Schema:
        record = {c:self.__db[c][ID] for c in self.columns}
        return self.schema(**record)

    @_commitRecorder
    def insert(self, s: Schema) -> DBCreate:
        print(type(s))
        return DBCreate(record=s)

    @_commitRecorder
    def update(self, s: Schema, updated_fields: List[str]) -> DBUpdate:
        return DBUpdate(record=s,updated_fields=updated_fields)

    @_commitRecorder
    def delete(self, s: Schema) -> DBDelete:
        return DBUpdate(record=s)

    @property
    def columns(self) -> List[str]:
        return list(self.__db.keys())

    def commit(self):
        self._commiter(self._commit_list)
        del self

class DenManager(object):
    pass

