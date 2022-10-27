

from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject, ThrowError


class CSArray(CSObject):pass
class CSArray(CSObject):
    """
    """
    LENGTH= "length"
    PUSH  = "push"

    def __init__(self):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSArray
    
    def initializeBound(self):
        super().initializeBound()
        # === ARRAY Bounds|
        # ================|
        self.proto.put(CSArray.LENGTH, CSObject.new_bound_method(CSArray.LENGTH, self.length, 0))
        self.proto.put(CSArray.PUSH  , CSObject.new_bound_method(CSArray.PUSH  , self.push  , 1))
    
    #![bound::length]
    def length(self):
        """ Get array length

            Returns
            -------
            CSInteger
        """
        return CSObject.new_integer(len(self.all()))

    #![bound::push]
    def push(self, _csobject:CSObject):
        """ Push new item into array

            Returns
            -------
            CSObject
        """
        # put element
        self.thiso.put(str(len(self.all())), _csobject)
    
        # default return
        return CSObject.new_nulltype()
    
    # ![bound::pop]
    def pop(self, _csobject:CSObject):
        """ Pop item into array

            Returns
            -------
            CSObject
        """
    
    # ======================== PYTHON|
    # ===============================|

    def python(self):
        _lst = []
        for _obj in self.all():
            _lst.append(_obj.python())
        
        return _lst

    def __str__(self):
        _elem = ""
        for idx in range(len(self.all())):
            _string = ...
            if  self.offset == self.thiso.get(str(idx)).offset:
                # refering to its self
                # to avoid recursion
                _string = "[self]"
            else:
                _string = self.thiso.get(str(idx)).__str__()

            _elem += _string

            if  idx < (len(self.all()) - 1):
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
        if  _expr.dtype != CSClassNames.CSInteger:
            # = format string|
            _error = CSObject.new_type_error("CSArray subscript must be a type of CSInteger", _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        if  not self.thiso.hasKey(_expr.__str__()):
            _opt = "<" if len(self.thiso.all()) < _expr.get("this") else ">"
            _lhs = len(self.thiso.all()) if _opt == "<" else 0

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
        
        return self.thiso.get(_expr.__str__())
    
    def subscriptSet(self, _subscript_location: CSToken, _attribute: CSObject, _new_value: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _attribute)
        if _error: return _error

        self.thiso.put(_attribute.__str__(), _new_value)

        return self.thiso.get(_attribute.__str__())



