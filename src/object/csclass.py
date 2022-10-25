from csclassnames import CSClassNames
from csmap import CSMap
from csobject import CSMalloc, CSObject

# method
from csclassmethod import CSClassMethod
from cstoken import CSToken

class CSClass(CSObject):

    def __init__(self, _name:str):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSClass
        self.name  = _name

        # default
    
    def __str__(self):
        return "class %s{...}" % self.name
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte

    def new_op(self, _opt:CSToken, _allocate:bool=True):
        """ 1(new Animals) 2(1,2,3)
        """
        _instance = CSMalloc(CSClassInstance(self.name))
    
        for _key in self.keys():
            _instance.put(_key, self.get(_key))
        return _instance


class CSClassInstance(CSClass):
    """ Holds class instanciation

        Parameters
        ----------
        _name : str
    """

    def __init__(self, _name: str):
        super().__init__(_name)
        self.dtype = CSClassNames.CSClass
    
    # ======================== PYTHON|
    # ===============================|
    
    def put(self, _key: str, _data:CSObject):
        if  _data.dtype == CSClassNames.CSCallable:
            # wrap as method
            return super().put(_key, CSClassMethod(self, _data))
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