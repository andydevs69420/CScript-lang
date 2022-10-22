from csobject import CSToken, CSObject, CSMalloc, ThrowError, reformatError

class CSString(CSObject):
    """ String backend for CScript

        Paramters
        ---------
        _str : str
    """

    def __init__(self, _str:str):
        super().__init__()
        self.put("this", str(_str))

    # ![bound::toString]
    def toString(self):
        return self
    
    # ============ PYTHON|
    # ===================|
    
    def __str__(self):
        return self.get("this")
    
    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
    def add(self, _opt:CSToken, _object:CSObject):
        if  _object.dtype != "CSString":
           # = format string|
            _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

            # == throw error|
            # ==============|
            ThrowError(_error)

            # = return error|
            # ==============|
            return _error
        
        return CSObject.new_string(self.get("this") + _object.get("this"))