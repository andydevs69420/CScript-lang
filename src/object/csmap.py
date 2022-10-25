
from csclassnames import CSClassNames
from csobject import CSObject, ThrowError
from cstoken import CSToken

""" CSObject|Hashmap wrapper

    Use CSMap instead of object directly!
"""

class CSMap(CSObject):
    def __init__(self):
        super().__init__()
        self.initializeBound()
        
        self.dtype    = CSClassNames.CSMap 
        self.elements = CSObject.new(_allocate=False)
    
    def initializeBound(self):
        super().initializeBound()
        # ===== MAP Bounds|
        # ================|


    
    # ======================== PYTHON|
    # ===============================|

    def keys(self):
        return self.elements.keys()

    def put(self, _key: str, _data):
        self.elements.put(_key, _data)
    
    def get(self, _key: str):
        return self.elements.get(_key)
    
    def all(self):
        return self.elements.all()

    def isPointer(self):
        return True
    
    def __str__(self):
        _keys   = self.elements.keys()
        _attrib = ""
        for k in range(len(_keys)):
            _string = ...
            if  self.offset == self.elements.get(_keys[k]).offset:
                # refering to its self
                # to avoid recursion
                _string = "{self}"
            else:
                _string = self.elements.get(_keys[k]).__str__()

            _attrib += f"{_keys[k]}: {_string}"

            if  k < (len(_keys) - 1):
                _attrib += ", "

        return "{" + f"{_attrib}" + "}"
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    def assertSubscriptExpression(self, _subscript_location: CSToken, _expr:CSObject):
        if  _expr.dtype != "CSString":
            # = format string|
            _error = CSObject.new_type_error("CSMap subscript must be a type of CSString", _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        if  not self.elements.hasAttribute(_expr.__str__()):
            # = format string|
            _error = CSObject.new_attrib_error(f"CSMap({self.elements.__str__()}) has no attribute %s" % _expr.__str__(), _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        return False
    
    def getAttribute(self, _attr: CSToken):
        return self.elements.getAttribute(_attr)
    
    def setAttribute(self, _attr: CSToken, _value: CSObject):
        return self.elements.setAttribute(_attr, _value)
    
    def subscript(self, _subscript_location: CSToken, _expr: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _expr)
        if _error: return _error

        return self.elements.get(_expr.__str__())
    
    def subscriptSet(self, _subscript_location: CSToken, _attribute: CSObject, _new_value: CSObject):
        if  _attribute.dtype != "CSString":
            # = format string|
            _error = CSObject.new_type_error("CSMap subscript must be a type of CSString", _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error

        self.elements.put(_attribute.__str__(), _new_value)
        return self.elements.get(_attribute.__str__())

    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte