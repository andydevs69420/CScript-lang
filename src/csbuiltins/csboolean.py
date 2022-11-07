




from csbuiltins.cstypes import CSTypes
from .base.csobject import CSObject


class CSBoolean(CSObject):
    """ Handles boolean datatype

        Parameters
        ----------
        _raw_py_bool : bool
    """
    
    def __init__(self, _raw_py_bool:bool):
        super().__init__()
        assert type(_raw_py_bool) == bool, "invalid boolean value %s" % _raw_py_bool
        self.type = CSTypes.TYPE_CSBOOLEAN
        self.this = bool(_raw_py_bool)\
            if type(_raw_py_bool) != bool else _raw_py_bool
    
    def __str__(self):
        return "%s" % ("true" if self.this else "false")
