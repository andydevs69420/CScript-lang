
from obj_utils.csclassnames import CSClassNames
from base.csobject import CSObject, CSToken


class CSException(CSObject):
    def __init__(self, _message:str, _token_loc:CSToken):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSException
        self.put("message" , CSObject.new_string(_message))
        self.put("location", CSObject.new_map_fromPyDict(_token_loc.toDict()))
    
    def isPointer(self):
        return True
    
    # ======================== PYTHON|
    # ===============================|

    def __str__(self):
        return reformatError(self.dtype, self.get("message"), self.get("location"))


class CSTypeError(CSException):
    def __init__(self, _message:str, _token_loc:CSToken):
        super().__init__(_message, _token_loc)
        self.dtype = CSClassNames.CSTypeError

class CSAttributeError(CSException):
    def __init__(self, _message: str, _token_loc: CSToken):
        super().__init__(_message, _token_loc)
        self.dtype = CSClassNames.CSAttributeError

class CSIndexError(CSException):
    def __init__(self, _message: str, _token_loc: CSToken):
        super().__init__(_message, _token_loc)
        self.dtype = CSClassNames.CSDouble


def reformatError(_type, _message:CSObject, _token:CSObject):
    """ By default, the entire error is string, not an exception.

        Prameters
        ---------
        _csexceptionobject : CSObject
        _token             : CSToken
    """
    _error = (("[%s:%d:%d] %s: %s" % (_token.get("fsrce").get("this"), _token.get("yS").get("this"), _token.get("xS").get("this"), _type, _message.get("this")))
             + "\n" 
             + _token.get("trace").__str__())
    return _error
