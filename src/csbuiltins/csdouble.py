

from csbuiltins.base.csobject import CSObject
from csbuiltins.cstypes import CSTypes


class CSDouble(CSObject):
    """ Represents double in cscript

        Parameters
        ----------
        _raw_py_float: float
    """

    def __init__(self, _raw_py_float:float):
        super().__init__()
        self.type = CSTypes.TYPE_CSDOUBLE
        self.this = float(_raw_py_float)\
            if type(_raw_py_float) != float else _raw_py_float

    def __str__(self):
        return "%.2f" % self.this