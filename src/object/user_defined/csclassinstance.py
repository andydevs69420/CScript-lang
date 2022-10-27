
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
            # === wrap as method|
            # ==================|
            self.thiso.put(_key, CSObject.new_class_bound_method(self, _data))
            return
        # default object #
        self.thiso.put(_key, _data)
    
    def __str__(self):
        return "instanceOf %s({...});" % self.name
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    
    def call(self, _call_location: CSToken, _arg_count: int):
        if  self.thiso.hasKey(CSClass.CONSTRUCTOR):
            self.thiso\
                .get(CSClass.CONSTRUCTOR)\
                    .call(_call_location, _arg_count)
        else:
            self.proto\
                .get(CSClass.CONSTRUCTOR)\
                    .call(_call_location, _arg_count)
        return self
    
    # ===================== OPERATION|
    # ===============================|
    # must be private!. do not include as attribute

    def new_op(self, _opt: CSToken):
        return CSObject.new_op(self, _opt)
    
    def eq(self, _opt: CSToken, _object: CSObject):
        return CSObject.new_boolean("true" if self.offset == _object.offset else "false")

    def neq(self, _opt: CSToken, _object: CSObject):
        return CSObject.new_boolean("true" if self.offset != _object.offset else "false")