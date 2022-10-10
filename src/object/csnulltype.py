
from types import NoneType
from csobject import CSObject


class CSNullType(CSObject):
    """NullType backend for CScript

        Paramters
        ---------
        _null : NoneType
    """

    def __init__(self, _null:NoneType):
        super().__init__()
        self.put("this", None)

    # ![bound::toString]
    def toString(self):
        return str("null")

