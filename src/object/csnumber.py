
from csobject import CSObject


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
        return str(self.get("this"))
    
    # =============================== MAGIC METHODS
    def bit_not(self):
        return CSObject.new_integer(~ self.get("this"))

    def bin_not(self):
        return CSObject.new_boolean("true" if not self.get("this") else "false")
    
    def positive(self):
        return CSObject.new_integer(+ self.get("this"))
    
    def negative(self):
        return CSObject.new_integer(- self.get("this"))

    def pow(self, _object:CSObject):
        _class = None

        if  _object.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _object.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # TODO: error!
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % ("^^", self.dtype, _object.dtype))
        
        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double
        
        return _class(self.get("this") ** _object.get("this"))

    def mul(self, _object:CSObject):
        _class = None

        if  _object.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _object.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # TODO: error!
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % ("*", self.dtype, _object.dtype))
        
        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double
        
        return _class(self.get("this") * _object.get("this"))
    

    def div(self, _object:CSObject):
        _class = None

        if  _object.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _object.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # TODO: error!
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % ("/", self.dtype, _object.dtype))
        
        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double

        _left  = self.get("this")
        _right = _object.get("this")

        # TODO: check division error

        return _class(_left / _right)
    
    def mod(self, _object:CSObject):
        _class = None

        if  _object.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _object.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # TODO: error!
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % ("%", self.dtype, _object.dtype))
        
        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double

        _left  = self.get("this")
        _right = _object.get("this")

        # TODO: check division error

        return _class(_left % _right)

    def add(self, _object:CSObject):
        _class = None

        if  _object.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _object.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # TODO: error!
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % ("+", self.dtype, _object.dtype))

        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double
        
        return _class(self.get("this") + _object.get("this"))
    
    def sub(self, _object:CSObject):
        _class = None

        if  _object.dtype == "CSInteger":
            _class = CSObject.new_integer
        elif _object.dtype == "CSDouble":
            _class = CSObject.new_double
        else:
            # TODO: error!
            raise TypeError("unsupported op '%s' for type(s) %s and %s" % ("-", self.dtype, _object.dtype))
        
        if  self.dtype == "CSDouble":\
        _class = CSObject.new_double

        return _class(self.get("this") - _object.get("this"))