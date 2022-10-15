
from csnumber import CSNumber
from csobject import CSObject
from cstoken import CSToken


class CSInteger(CSNumber):
    """ Integer backend for CScript

        Paramters
        ---------
        _int : int
    """

    def __init__(self, _int:int):
        super().__init__()
        self.put("this", int(_int))
    
    # ==================== MAGIC METHODS
    # ==================================
    """ CSInteger specific operation
    """
    def bit_not(self, _opt:CSToken):
        return CSObject.new_integer(~ self.get("this"))
    
    def lshift(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") << _object.get("this"))
    
    def rshift(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") >> _object.get("this"))
    
    def bit_and(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") & _object.get("this"))

    def bit_xor(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") ^ _object.get("this"))
    
    def bit_or(self, _opt:CSToken, _object:CSObject):
        _class = self.assertType(_opt, self, _object)
        return _class(self.get("this") | _object.get("this"))