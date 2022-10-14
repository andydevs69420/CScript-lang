
from types import NoneType
from csobject import CSObject
from cstoken import CSToken


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
        return CSObject.new_string("null")
    
    # ==================== MAGIC METHODS
    """ CSInteger specific operation
    """
    def bin_not(self, _opt:CSToken):
        return CSObject.new_boolean("true" if not self.get("this") else "false")
