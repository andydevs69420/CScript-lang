
from csobject import CSObject


class CSString(CSObject):
    """ String backend for CScript

        Paramters
        ---------
        _str : str
    """

    def __init__(self, _str:str):
        super().__init__()
        # 
        self.put("this", str(_str))

    # ![bound::toString]
    def toString(self):
        return str(self.get("this"))
    
    # =============================== MAGIC METHODS
    def add(self, _object:CSObject):
        if  _object.dtype != "CSString":
            # TODO: error!
            return
        
        return CSObject.new_string(self.get("this") + _object.get("this"))