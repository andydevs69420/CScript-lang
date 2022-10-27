from base.csobject import CSToken, CSObject, ThrowError
from obj_utils.nonpointer import NonPointer


class CSNumber(NonPointer):
    """ Integer|Double backend for CScript

        Parameters
        ---------
        _int : int
    """
    THIS= "this"

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "%d" % self.thiso.get(CSNumber.THIS)
    
    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
    def assertType(self, _opt:CSToken, _lhs:CSObject, _rhs:CSObject):
        _class = None

        if  _rhs.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _rhs.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # = format string|
            _error = CSObject.new_type_error("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, _lhs.dtype, _rhs.dtype), _opt)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        # follow left-hand if double
        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double

        return _class
    """
        Shared operation for numbers
    """
    def bin_not(self, _opt:CSToken):
        return CSObject.new_boolean("true" if not self.python() else "false")
    
    def positive(self, _opt:CSToken):
        return CSObject.new_integer(+ self.python())
    
    def negative(self, _opt:CSToken):
        return CSObject.new_integer(- self.python())

    def pow(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.python() ** _object.python())

    def mul(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.python() * _object.python())
    

    def div(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)

        _left  = self.python()
        _right = _object.python()

        # TODO: check division error

        return _class(_left / _right)
    
    def mod(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)

        _left  = self.python()
        _right = _object.python()

        # TODO: check division error

        return _class(_left % _right)

    def add(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.python() + _object.python())
    
    def sub(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.python() - _object.python())
    
    def lt(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() < _object.python() else "false")
    
    def lte(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() <= _object.python() else "false")

    def gt(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() > _object.python() else "false")
    
    def gte(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() >= _object.python() else "false")

    def eq(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() == _object.python() else "false")
    
    def neq(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.python() != _object.python() else "false")