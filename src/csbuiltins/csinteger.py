

# .
from csbuiltins.cstypes import CSTypes
from .base.csobject import CSObject


class CSInteger(CSObject):
    """ Represents integer in cscript

        Parameters
        ----------
        _raw_py_int : int
    """

    def __init__(self, _raw_py_int:int):
        super().__init__()
        self.type = CSTypes.TYPE_CSINTEGER
        self.this = int(_raw_py_int)\
            if type(_raw_py_int) != int else _raw_py_int
    
    def __get__(self):
        return self.type

    def __str__(self):
        return "%d" % self.this