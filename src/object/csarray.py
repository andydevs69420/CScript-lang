


from csobject import CSToken, CSObject, ThrowError


class CSArray(CSObject):pass
class CSArray(CSObject):

    def __init__(self):
        super().__init__()
        self.put("length"  , CSObject.new_integer(0))
        self.put("elements", CSObject())
    
    # ![bound::push]
    def push(self, _csobject:CSObject):
        """ Push new item into array

            Returns
            -------
            CSObject
        """
        _old_size = self.get("length")\
            .get("this")

        # put element
        self.get("elements")\
            .put(_old_size.__str__(), _csobject)

        # update size
        self.put("length", CSObject.new_integer(_old_size + 1))
    
        # default return
        return CSObject.new_nulltype()
    
    # ![bound::pop]
    def pop(self, _csobject:CSObject):
        """ Pop item into array

            Returns
            -------
            CSObject
        """
    
    # ============ PYTHON|
    # ===================|
    
    def all(self):
        return self.get("elements").all()
    
    def isPointer(self):
        return True

    def __str__(self):
        _elem = ""
        for idx in range(self.get("length").get("this")):
            _elem += str(self.get("elements").get(str(idx)))

            if  idx < (self.get("length").get("this") - 1):
                _elem += ", "
        
        # return formated string
        return "[" + _elem + "]"

    def reBuild(self):
        """ Rebuilds array when pop is called
        """
        return
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
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

        if  not self.get("elements").hasAttribute(str(_expr.get("this"))):
            # = format string|
            _error = reformatError("CSArray index out of range %d < %d" % (self.get("length").get("this"), _expr.get("this")), _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        return self.get("elements").get(str(_expr.get("this")))
            



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


