from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject, ThrowError

class CSString(CSObject):
    """ String backend for CScript

        Paramters
        ---------
        _str : str
    """

    def __init__(self, _str:str):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSString
        self.put("this", str(_str))

    # ![bound::toString]
    def toString(self):
        return self
    
    # ======================== PYTHON|
    # ===============================|
    
    def __str__(self):
        return self.get("this")
    
    def __repr__(self) -> str:
        return "\"" + self.__str__() + "\""
    
    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
    def add(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        if  _object.dtype != "CSString":
           # = format string|
            _error = CSObject.new_type_error("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

            # == throw error|
            # ==============|
            ThrowError(_error)

            # = return error|
            # ==============|
            return _error
        
        return CSObject.new_string(self.get("this") + _object.get("this"))
    
    def eq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.get("this") == _object.get("this") else "false")
    
    def neq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.get("this") != _object.get("this") else "false")