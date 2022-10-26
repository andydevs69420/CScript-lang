
from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject, ThrowError


class CSBoolean(CSObject):
    """ Boolean backend for CScript

        Paramters
        ---------
        _bool : boolean
    """

    def __init__(self, _bool:str):
        assert _bool in ("true", "false"), "invalid boolean value(%s)" % _bool
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSBoolean
        self.put("this", True if _bool == "true" else False)
    
    # ======================== PYTHON|
    # ===============================|

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
    def bin_not(self, _opt:CSToken):
        return CSObject.new_boolean("true" if not self.get("this") else "false")
    
    def eq(self, _opt: CSToken, _object: CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") == _object.get("this") else "false")
    
    def neq(self, _opt: CSToken, _object: CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") != _object.get("this") else "false")
