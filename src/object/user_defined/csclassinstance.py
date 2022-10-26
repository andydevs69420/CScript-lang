
from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject


from .csclass import CSClass
from .csclassboundmethod import CSClassBoundMethod

class CSClassInstance(CSClass):
    """ Holds class instanciation

        Parameters
        ----------
        _name : str
    """

    def __init__(self, _name: str):
        super().__init__(_name)
    
    # ======================== PYTHON|
    # ===============================|
    
    def put(self, _key: str, _data:CSObject):
        if  _data.dtype == CSClassNames.CSCallable:
            # wrap as method
            super().put(_key, CSClassBoundMethod(self, _data))
            return
        # default
        return super().put(_key, _data)
    
    def __str__(self):
        return "instanceOf %s({...});" % self.name
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    
    def call(self, _call_location: CSToken, _arg_count: int):
        self.get("constructor").call(_call_location, _arg_count)
        return self
    
    # ===================== OPERATION|
    # ===============================|
    # must be private!. do not include as attribute
    
    def eq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.offset == _object.offset else "false", _allocate)

    def neq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.offset != _object.offset else "false", _allocate)