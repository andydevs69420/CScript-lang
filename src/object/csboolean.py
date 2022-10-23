
from csobject import CSToken, CSObject, CSMalloc, ThrowError


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
    
    # ============ PYTHON|
    # ===================|

    def __str__(self):
        return "true" if self.get("this") else "false"
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    
    def assertType(self, _opt: CSToken, _lhs: CSObject, _rhs: CSObject):
        if  _lhs.dtype != _rhs.dtype:
            # = format string|
            _error = CSObject.new_type_error("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, _lhs.dtype, _rhs.dtype), _opt)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error

        # return success
        return True
    # ===================== OPERATION|
    # ===============================|
    # must be private!. do not include as attribte
    
    """ CSBoolean specific operation
    """
    def bin_not(self, _opt:CSToken, _allocate:bool=True):
        return CSObject.new_boolean("true" if not self.get("this") else "false", _allocate)
    
    def eq(self, _opt: CSToken, _object: CSObject, _allocate:bool=True):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") == _object.get("this") else "false", _allocate)
    
    def neq(self, _opt: CSToken, _object: CSObject, _allocate:bool=True):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") != _object.get("this") else "false", _allocate)
    
    def log_and(self, _opt: CSToken, _object: CSObject, _allocate:bool=True):
        # self.assertType(_opt, self, _object)
        # TODO: fix!!!!! memory hungry!
        return CSMalloc(_object if self.get("this") and _object.get("this") else self, _allocate)
    
    def log_or(self, _opt: CSToken, _object: CSObject, _allocate:bool=True):
        # self.assertType(_opt, self, _object)
        # TODO: fix!!!!! memory hungry!
        return CSMalloc(self if self.get("this") or _object.get("this") else _object, _allocate)
