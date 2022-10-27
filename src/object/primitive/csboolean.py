
from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject, ThrowError
from obj_utils.nonpointer import NonPointer


class CSBoolean(NonPointer):
    """ Boolean backend for CScript

        Paramters
        ---------
        _bool : boolean
    """
    THIS= "this"

    def __init__(self, _bool:str):
        assert _bool in ("true", "false"), "invalid boolean value(%s)" % _bool
        super().__init__()

        self.dtype = CSClassNames.CSBoolean
        self.thiso.put(CSBoolean.THIS, True if _bool == "true" else False)
    
    def __str__(self):
        return "true" if self.python() else "false"
    
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
        return CSObject.new_boolean("true" if not self.python() else "false")
    
    def eq(self, _opt: CSToken, _object: CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() == _object.python() else "false")
    
    def neq(self, _opt: CSToken, _object: CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() != _object.python() else "false")
