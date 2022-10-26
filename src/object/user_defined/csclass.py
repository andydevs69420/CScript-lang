
from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject



class CSClass(CSObject):

    def __init__(self, _name:str):
        super().__init__()
        self.initializeBound()

        self.dtype = CSClassNames.CSClass
        self.name  = _name

    # ======================== PYTHON|
    # ===============================|
    
    def initializeBound(self):
        super().initializeBound()
        # ==== CLASS INSTANCE Bounds|
        # ==========================|
        self.put("constructor", CSObject.new_bound_method("constructor", self.constructor, 0))

    #![bound::constructor]
    def constructor(self):
        return CSObject.new_nulltype()
    
    def isPointer(self):
        return True
    
    def __str__(self):
        return "class %s{...}" % self.name
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte

    def new_op(self, _opt:CSToken, _allocate:bool=True):
        """ 1(new Animals) 2(1,2,3)
        """
        _instance = CSObject.new_class_instance(self.name)
    
        for _key in self.keys():
            _instance.put(_key, self.get(_key))
        return _instance


