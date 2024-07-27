from typing import  Any
from typing import NewType

from pydantic import BaseModel as BsMdl

ID = NewType('ID', int)
COLUMN = NewType('COLUMN', str)
LEVEL = NewType('LEVEL', str)

class BaseModel(BsMdl):
    class Config:
        arbitrary_types_allowed = True
        
def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)