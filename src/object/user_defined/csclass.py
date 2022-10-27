
from obj_utils.csclassnames import CSClassNames
from non_primitive.csmap import CSMap
from base.csobject import CSToken, CSObject



class CSClass(CSMap):
    """
    """
    CONSTRUCTOR= "constructor"

    def __init__(self, _name:str):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSClass
        self.name  = _name
    
    def initializeBound(self):
        super().initializeBound()
        # ==== CLASS INSTANCE Bounds|
        # ==========================|
        self.proto.put(CSClass.CONSTRUCTOR, CSObject.new_bound_method(CSClass.CONSTRUCTOR, self.constructor, 0))

    # ======================== BOUNDS|
    # ===============================|

    #![bound::constructor]
    def constructor(self):
        return CSObject.new_nulltype()
    
    # ======================== PYTHON|
    # ===============================|
    
    def __str__(self):
        return "class %s{...}" % self.name
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte

    def new_op(self, _opt:CSToken, _allocate:bool=True):
        """ 1(new Animals) 2(1,2,3)
        """
        _instance = CSObject.new_class_instance(self.name)
    
        for _key in self.thiso.keys():
            _instance.put(_key, self.thiso.get(_key))
        return _instance


