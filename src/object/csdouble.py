
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