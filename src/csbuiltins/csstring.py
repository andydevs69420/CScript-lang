



# .
from csbuiltins.cstypes import CSTypes
from .base.csobject import CSObject


class CSString(CSObject):
    """ Represents string for cscript
    """

    def __init__(self, _raw_py_string:str):
        super().__init__()
        self.type = CSTypes.TYPE_CSSTRING
        self.this = str(_raw_py_string)\
            if type(_raw_py_string) != str else _raw_py_string

    def __str__(self):
        return self.this
