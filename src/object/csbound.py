

from csobject import CSObject, ThrowError
from cstoken import CSToken


class CSBound(CSObject):
    """
    """

    def __init__(self, _pyMethod:callable, _param_count:int):
        super().__init__()        
        self.callable    = _pyMethod
        self.param_count = _param_count
    
    # ======================== PYTHON|
    # ===============================|
    def __str__(self):
        return "bound method(){...}"
    

    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte

    def call(self, _call_location: CSToken, _arg_count: int):
        if  self.param_count != _arg_count:
            # = format string|
            _error = CSObject.new_type_error("expected parameter count %d, got %d" % (self.param_count, _arg_count), _call_location)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        # call
        from cscriptvm.csvm import EvalStack as ES
        _args = [
            # 0
            # 1
            # N
        ]

        for _ in range(_arg_count):
            _args.append(ES.es_pop())

        # delete ES locally
        del ES
        return self.callable(*_args)

