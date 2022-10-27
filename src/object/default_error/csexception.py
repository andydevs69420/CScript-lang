
from obj_utils.csclassnames import CSClassNames
from base.csobject import CSObject, CSToken


class CSException(CSObject):
    def __init__(self, _message:str, _token_loc:CSToken):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSException
        self.thiso.put("message" , CSObject.new_string(_message))
        self.thiso.put("location", CSObject.new_map_fromPyDict(_token_loc.toDict()))
    
    # ======================== PYTHON|
    # ===============================|

    def __str__(self):
        return reformatError(self.dtype, self.thiso.get("message"), self.thiso.get("location"))


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
    _map = _token.python()

    _error = (("[%s:%d:%d] %s: %s" % (_map["fsrce"], _map["yS"], _map["xS"], _type, _message.python()))
             + "\n" 
             + _map["trace"])
    return _error
