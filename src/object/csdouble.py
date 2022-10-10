
from csnumber import CSNumber
from csobject import CSObject


class CSDouble(CSNumber):
    """ Double backend for CScript

        Paramters
        ---------
        _flt : float
    """

    def __init__(self, _flt:float):
        super().__init__()
        # 
        self.put("this", float(_flt))
    
    # ![bound::toString]
    def toString(self):
        return str(self.get("this"))
    
    # ======================== OVERRIDE MAGIC METHOD
    def bit_not(self):
        ...
        # TODO: add error !
        raise TypeError("invalid bitwise expression for non integer!")
    def bit_and(self):
        ...
        # TODO: add error !
        raise TypeError("invalid bitwise expression for non integer!")
    
    def bit_xor(self):
        ...
        # TODO: add error !
        raise TypeError("invalid bitwise expression for non integer!")
    
    def bit_or(self, _object: CSObject):
        ...
        # TODO: add error !
        raise TypeError("invalid bitwise expression for non integer!")