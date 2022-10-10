


from csobject import CSObject


class CSBoolean(CSObject):
    """ Boolean backend for CScript

        Paramters
        ---------
        _bool : boolean
    """

    def __init__(self, _bool:str):
        assert _bool in ("true", "false"), "invalid boolean value(%s)" % _bool
        super().__init__()
        self.put("this", bool(True if _bool == "true" else False))
    
    # ![bound::toString]
    def toString(self):
        return "true" if self.get("this") else "false"
    
    # ================= MAGIC METHODS
    def bin_not(self):
        return CSObject.new_boolean("true" if not self.get("this") else "false")
