


from csobject import CSToken, CSObject, ThrowError


class CSArray(CSObject):pass
class CSArray(CSObject):

    def __init__(self):
        super().__init__()
        self.put("length"  , CSObject.new_integer(0))
        self.put("elements", CSObject.new_map())
    
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
        return [self.get(k) for k in self.keys()]
    
    def isPointer(self):
        return True

    def __str__(self):
        _elem = ""
        for idx in range(self.get("length").get("this")):
            _elem += self.get("elements").get(str(idx)).__str__()

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
        
        if  not self.get("elements").hasAttribute(_expr.__str__()):
            _opt = "<" if self.get("length").get("this") < _expr.get("this") else ">"
            _lhs = self.get("length").get("this") if _opt == "<" else 0
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
        
        return self.get("elements").get(_expr.__str__())
    
    def subscriptSet(self, _subscript_location: CSToken, _attribute: CSObject, _new_value: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _attribute)
        if _error: return _error

        self.get("elements").put(_attribute.__str__(), _new_value)

        return self.get("elements").get(_attribute.__str__())



