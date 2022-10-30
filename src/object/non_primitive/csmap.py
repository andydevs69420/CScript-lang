from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject, ThrowError

""" CSObject|Hashmap wrapper

    Use CSMap instead of object directly!
"""

class CSMap(CSObject):
    def __init__(self):
        super().__init__()
        self.initializeBound()
        
        self.dtype = CSClassNames.CSMap 
    
    def initializeBound(self):
        super().initializeBound()
        # ===== MAP Bounds|
        # ================|


    # ======================== PYTHON|
    # ===============================|

    def keys(self):
        return self.thiso.keys()

    def put(self, _key: str, _data):
        self.thiso.put(_key, _data)
    
    def get(self, _key: str):
        return self.thiso.get(_key)
    
    def python(self):
        _map = ({})
        for _k, _v in zip(self.keys(), self.all()):
            _map[_k] = _v.python()
        
        return _map
    
    def __str__(self):
        # print(self.offset)
        _keys   = self.keys()
        _attrib = ""
        for k in range(len(_keys)):
            _string = ...
            if  self.offset == self.thiso.get(_keys[k]).offset and self.offset >= 0:
                # refering to its self
                # to avoid recursion
                _string = "{self}"
            else:
                _string = self.thiso.get(_keys[k]).__str__()

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
        
        if  not self.thiso.hasKey(_expr.__str__()):
            # = format string|
            _error = CSObject.new_attrib_error(f"CSMap({self.thiso.__str__()}) has no attribute %s" % _expr.__str__(), _subscript_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        return False
    
    def getAttribute(self, _attr: CSToken):
        return super().getAttribute(_attr)
    
    def setAttribute(self, _attr: CSToken, _value: CSObject):
        return super().setAttribute(_attr, _value)
    
    def subscript(self, _subscript_location: CSToken, _expr: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _expr)
        if _error: return _error

        return self.thiso.get(_expr.__str__())
    
    def subscriptSet(self, _subscript_location: CSToken, _attribute: CSObject, _new_value: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _attribute)
        if _error: return _error

        self.thiso.put(_attribute.__str__(), _new_value)
        return self.thiso.get(_attribute.__str__())

    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte