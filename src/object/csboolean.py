


from csobject import CSObject
from cstoken import CSToken


class CSBoolean(CSObject):
    """ Boolean backend for CScript

        Paramters
        ---------
        _bool : boolean
    """

    def __init__(self, _bool:str):
        assert _bool in ("true", "false"), "invalid boolean value(%s)" % _bool
        super().__init__()
        self.put("this", bool(True if _bool == "true" else False))
    
    # ![bound::toString]
    def toString(self):
        return "true" if self.get("this") else "false"
    
    # ================= SUPPORTED MAGIC METHODS
    def assertType(self, _opt: CSToken, _lhs: CSObject, _rhs: CSObject):
        if  _lhs.dtype != _rhs.dtype:
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % (_opt.token, _lhs.dtype, _rhs.dtype))
        return True
    """ CSBoolean specific operation
    """
    def bin_not(self, _opt:CSToken):
        return CSObject.new_boolean("true" if not self.get("this") else "false")
    
    def log_and(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") and _object.get("this") else "false")
    
    def log_or(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") or _object.get("this") else "false")
