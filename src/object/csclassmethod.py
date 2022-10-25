
from cscallable import CSCallable
from csclassnames import CSClassNames
from csobject import CSObject
from cstoken import CSToken

class CSClassMethod(CSObject):
    
    def __init__(self, _this:CSObject, _regular_callable:CSCallable):
        super().__init__()
        self.initializeBound()

        self.dtype    = CSClassNames.CSClassMethod
        self.thisref  = _this
        self.callable = _regular_callable

    # ======================== PYTHON|
    # ===============================|

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
        return CSObject.new_boolean("true" if self.offset == _object.offset else "false", _allocate)

    def neq(self, _opt: CSToken, _object: CSObject, _allocate: bool = True):
        return CSObject.new_boolean("true" if self.offset != _object.offset else "false", _allocate)