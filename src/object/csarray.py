

from csobject import CSToken, CSObject, ThrowError


class CSArray(CSObject):pass
class CSArray(CSObject):

    def __init__(self):
        super().__init__()
        self.elements = CSObject.new_map(_allocate=False)
    
    # ![bound::length]
    def length(self):
        return CSObject.new_integer(len(self.elements.all()))

    # ![bound::push]
    def push(self, _csobject:CSObject):
        """ Push new item into array

            Returns
            -------
            CSObject
        """
        # put element
        self.elements.elements.put(str(len(self.elements.all())), _csobject)
    
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
        return self.elements.all()
    
    def isPointer(self):
        return True

    def __str__(self):
        _elem = ""
        for idx in range(len(self.elements.all())):
            _string = ...
            if  self.offset == self.elements.elements.get(str(idx)).offset:
                # refering to its self
                # to avoid recursion
                _string = "{self}"
                _string = "[self]"
            else:
                _string = self.elements.elements.get(str(idx)).__str__()

            _elem += _string

            if  idx < (len(self.elements.all()) - 1):
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
    def assertSubscriptExpression(self, _subscript_location: CSToken, _expr:CSObject):
        if  _expr.dtype != "CSInteger":
            # = format string|
            _error = CSObject.new_type_error("CSArray subscript must be a type of CSInteger", _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        if  not self.elements.elements.hasAttribute(_expr.__str__()):
            _opt = "<" if len(self.elements.all()) < _expr.get("this") else ">"
            _lhs = len(self.elements.all()) if _opt == "<" else 0

            # = format string|
            _error = CSObject.new_index_error("CSArray index out of range %d %s %d" % (_lhs, _opt, _expr.get("this")), _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        return False

    def subscript(self, _subscript_location: CSToken, _expr: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _expr)
        if _error: return _error
        
        return self.elements.elements.get(_expr.__str__())
    
    def subscriptSet(self, _subscript_location: CSToken, _attribute: CSObject, _new_value: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _attribute)
        if _error: return _error

        self.elements.elements.put(_attribute.__str__(), _new_value)

        return self.elements.elements.get(_attribute.__str__())



