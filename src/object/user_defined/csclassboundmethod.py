
from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject


from user_defined.cscallable import CSCallable

class CSClassBoundMethod(CSObject):
    
    def __init__(self, _this:CSObject, _regular_callable:CSCallable):
        super().__init__()
        self.initializeBound()

        self.dtype    = CSClassNames.CSClassBoundMethod
        self.thisref  = _this
        self.callable = _regular_callable

    # ======================== PYTHON|
    # ===============================|

    def all(self):
        return [self.callable]

    def isPointer(self):
        return True

    def __str__(self):
        return self.callable.__str__()
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    def call(self, _call_location: CSToken, _arg_count: int):
        _actual_count:int = int(_arg_count)
        # core
        from cscriptvm.csvm import EvalStack as ES

        # push self on top
        if  self.callable.param_count != 0:
            # add 1 to parameter count
            _actual_count += 1
            ES.es_push(self.thisref)

        # delete vm locally
        del ES
        # append self as parameters list
        return self.callable.call(_call_location, _actual_count)

    # ===================== OPERATION|
    # ===============================|
    # must be private!. do not include as attribute

    def eq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.offset == _object.offset else "false")

    def neq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.offset != _object.offset else "false")