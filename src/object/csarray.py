


from csobject import CSToken, CSObject, CSMalloc, ThrowError, reformatError


class CSArray(CSObject):pass
class CSArray(CSObject):

    def __init__(self):
        super().__init__()
        self.size = 0
        self.elem = CSObject()
        self.put("length"  , self.size)
        self.put("elements", self.elem)
    
    # ![bound::push]
    def push(self, _csobject:CSObject):
        """ Push new item into array

            Returns
            -------
            CSObject
        """
        self.elem.put(str(self.size), _csobject)
        self.size += 1
    
        # default return
        return CSObject.new_nulltype()
    
    # ![bound::pop]
    def pop(self, _csobject:CSObject):
        """ Pop item into array

            Returns
            -------
            CSObject
        """
    
    def getElements(self):
        _children = []
        for i in self.elem.keys():
            _children.append(self.elem.get(i))
        return _children
    
    def isPointer(self):
        return True

    def __str__(self):
        _elem = ""
        for idx in range(self.size):
            _elem += str(self.elem.get(str(idx)))

            if  idx < (self.size - 1):
                _elem += ", "
        
        # return formated string
        return "[" + _elem + "]"

    def reBuild(self):
        """ Rebuilds array when pop is called
        """
        ...

    @staticmethod
    def fromArray(_array:CSArray):
        """ Creates a new array from existing array

            Returns
            -------
            CSArray
        """
    
    # 
    def subscript(self, _subscript_location: CSToken, _expr: CSObject):
        if  _expr.dtype != "CSInteger":
            # = format string|
            _error = reformatError("CSArray subscript must be a type of CSInteger", _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error

        if  not self.elem.hasAttribute(str(_expr.get("this"))):
            # = format string|
            _error = reformatError("CSArray index out of range %d < %d" % (self.size, _expr.get("this")), _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        return self.elem.get(str(_expr.get("this")))
            



def reformatError(_message:str, _token:CSToken):
    """ By default, the entire error is string, not an exception.

        Prameters
        ---------
        _csexceptionobject : CSObject
        _token             : CSToken
    """
    _error = CSObject.new_string(
        ("[%s:%d:%d] CSError: %s" % (_token.fsrce, _token.yS, _token.xS, _message))
        + "\n" 
        + _token.trace
    )
    return _error


