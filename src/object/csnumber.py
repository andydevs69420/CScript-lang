
from csobject import CSObject
from cstoken import CSToken


class CSNumber(CSObject):
    """ Integer|Double backend for CScript

        Parameters
        ---------
        _int : int
    """

    def __init__(self):
        super().__init__()

    # ![bound::toString]
    def toString(self):
        return CSObject.new_string(str(self.get("this")))
    
    # =============================== MAGIC METHODS
    def assertType(self, _opt:CSToken, _lhs:CSObject, _rhs:CSObject):
        _class = None

        if  _rhs.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _rhs.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # TODO: error!
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % (_opt.token, _lhs.dtype, _rhs.dtype))
        
        # follow left-hand if double
        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double

        return _class
    """
        Shared operation for numbers
    """
    def bin_not(self, _opt:CSToken):
        return CSObject.new_boolean("true" if not self.get("this") else "false")
    
    def positive(self, _opt:CSToken):
        return CSObject.new_integer(+ self.get("this"))
    
    def negative(self, _opt:CSToken):
        return CSObject.new_integer(- self.get("this"))

    def pow(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") ** _object.get("this"))

    def mul(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") * _object.get("this"))
    

    def div(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)

        _left  = self.get("this")
        _right = _object.get("this")

        # TODO: check division error

        return _class(_left / _right)
    
    def mod(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)

        _left  = self.get("this")
        _right = _object.get("this")

        # TODO: check division error

        return _class(_left % _right)

    def add(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") + _object.get("this"))
    
    def sub(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") - _object.get("this"))
    
    def lt(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") < _object.get("this") else "false")
    
    def lte(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") <= _object.get("this") else "false")

    def gt(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") > _object.get("this") else "false")
    
    def gte(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") >= _object.get("this") else "false")

    def eq(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") == _object.get("this") else "false")
    
    def neq(self, _opt:CSToken, _object:CSObject):
        self.assertType(_opt, self, _object)
        return CSObject.new_boolean("true" if self.get("this") != _object.get("this") else "false")