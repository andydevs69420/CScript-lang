from obj_utils.csclassnames import CSClassNames
from obj_utils.nonpointer import NonPointer
from base.csobject import CSToken, CSObject, ThrowError

""" In CScript, strings not a pointer
"""
class CSString(NonPointer):
    """ String backend for CScript

        Paramters
        ---------
        _str : str
    """
    THIS= "this"

    def __init__(self, _str:str):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSString
        self.thiso.put(CSString.THIS, str(_str))

    # ![bound::toString]
    def toString(self):
        return self
    
    # ======================== PYTHON|
    # ===============================|

    def __str__(self):
        return self.thiso.get(CSString.THIS)
    
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
        
        return CSObject.new_string(self.python() + _object.python())
    
    def eq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.python() == _object.python() else "false")
    
    def neq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.python() != _object.python() else "false")