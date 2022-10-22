
from csobject import CSObject, CSToken


class CSException(CSObject):
    def __init__(self, _message:CSObject, _token_loc:CSObject):
        super().__init__()
        self.put("message" , _message  )
        self.put("location", _token_loc)
    
    # ============ PYTHON|
    # ===================|

    def __str__(self):
        return reformatError(self.dtype, self.get("message").__str__(), self.token_loc)



class CSTypeError(CSException):
    def __init__(self, _message: CSObject):
        super().__init__(_message)


def reformatError(_type, _message:str, _token:CSToken):
    """ By default, the entire error is string, not an exception.

        Prameters
        ---------
        _csexceptionobject : CSObject
        _token             : CSToken
    """
    _error = CSObject.new_string(
        ("[%s:%d:%d] %s: %s" % (_token.fsrce, _token.yS, _token.xS, _type, _message))
        + "\n" 
        + _token.trace
    )
    return _error
