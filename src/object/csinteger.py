
from csnumber import CSNumber


class CSInteger(CSNumber):
    """ Integer backend for CScript

        Paramters
        ---------
        _int : int
    """

    def __init__(self, _int:int):
        super().__init__()
        self.put("this", int(_int))

    # ![bound::toString]
    def toString(self):
        return str(self.get("this"))