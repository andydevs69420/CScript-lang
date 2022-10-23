
from csobject import CSObject, ThrowError
from cstoken import CSToken

""" CSObject|Hashmap wrapper

    Use CSMap instead of object directly!
"""

class CSMap(CSObject):
    def __init__(self):
        super().__init__()
    
    # ============ PYTHON|
    # ===================|

    def all(self):
        return super().all()

    def isPointer(self):
        return True
    
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
        
        if  not self.hasAttribute(_expr.__str__()):
            # = format string|
            _error = CSObject.new_attrib_error(f"CSMap({self.__str__()}) has no attribute %s" % _expr.__str__(), _subscript_location)

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

        return self.get(_expr.__str__())
    
    def subscriptSet(self, _subscript_location: CSToken, _attribute: CSObject, _new_value: CSObject):
        _error = self.assertSubscriptExpression(_subscript_location, _attribute)
        if _error: return _error

        self.put(_attribute.__str__(), _new_value)
        return self.get(_attribute.__str__())

    # ==================== OPERATIONS|
    # ===============================|
    # must be private!. do not include as attribte
