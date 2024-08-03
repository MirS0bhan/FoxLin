from typing import  Any
import string,random

from pydantic import BaseModel as BsMdl


class BaseModel(BsMdl):
    class Config:
        arbitrary_types_allowed = True


class ItemBaseClass:
    def __getitem__(self, i) -> Any:
        return self.__dict__[i]

    def __setitem__(self, name, value):
        setattr(self, name, value)
        
def get_attr(obj, name) -> Any:
    return object.__getattribute__(obj, name)

def generate_random_name(length: int = 8) -> str:
    """Generate a random session name."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
