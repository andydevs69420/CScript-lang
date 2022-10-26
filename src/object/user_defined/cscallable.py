from obj_utils.csclassnames import CSClassNames
from base.csobject import CSToken, CSObject, ThrowError


class CSCallable(CSObject):
    """ CSCallable

        Paratemers
        ----------
        _name         : str
        _param_count  : int
        _parameters   : list
        _instructions : list
    """

    def __init__(self, _name:str, _param_count:int, _parameters:list, _instructions:list):
        super().__init__()
        self.initializeBound()

        self.dtype        = CSClassNames.CSCallable
        self.func_name    = _name
        self.param_count  = _param_count
        self.parameters   = _parameters
        self.instructions = _instructions
    
    # ======================== PYTHON|
    # ===============================|
    
    def __str__(self):
        _fmt_param = ""
        for idx in range(self.param_count):
            _fmt_param += self.parameters[idx]

            if  idx < self.param_count - 1:
                _fmt_param += ", "
        return "function %s(%s){...}" % (self.func_name, _fmt_param)

    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    def call(self, _opt:CSToken, _arg_count:int):

        if  _arg_count != self.param_count:
            # = format string|
            _error = CSObject.new_type_error("expected parameter count %d, got %d" % (self.param_count, _arg_count), _opt)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        # core
        from cscriptvm.csvm import CSVM as VM
        
        _obj = VM.run(self.instructions)
        
        del VM
        return _obj
