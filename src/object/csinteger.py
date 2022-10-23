
from csnumber import CSToken, CSObject, CSNumber


class CSInteger(CSNumber):
    """ Integer backend for CScript

        Paramters
        ---------
        _int : int
    """

    def __init__(self, _int:int):
        super().__init__()
        self.put("this", int(_int))
    
    # ============ PYTHON|
    # ===================|
    
    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
    """ CSInteger specific operation
    """
    def bit_not(self, _opt:CSToken, _allocate:bool=True):
        return CSObject.new_integer(~ self.get("this"), _allocate)
    
    def lshift(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        return CSObject.new_integer(self.get("this") << _object.get("this"), _allocate)
    
    def rshift(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        return CSObject.new_integer(self.get("this") >> _object.get("this"), _allocate)
    
    def bit_and(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        return CSObject.new_integer(self.get("this") & _object.get("this"), _allocate)

    def bit_xor(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        return CSObject.new_integer(self.get("this") ^ _object.get("this"), _allocate)
    
    def bit_or(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        return CSObject.new_integer(self.get("this") | _object.get("this"), _allocate)