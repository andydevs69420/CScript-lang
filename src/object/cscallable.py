from csobject import CSToken, CSObject, CSMalloc, ThrowError, reformatError


class CSCallable(CSObject):

    def __init__(self, _name:str, _param_count:int, _parameters:list, _instructions:list):
        super().__init__()
        self.name         = _name
        self.paramcount   = _param_count
        self.parameters   = _parameters
        self.instructions = _instructions
    
    def get(self, _key: str):
        if  type(self) == CSCallable and _key == "this":
            return self
        return self.get(_key)
    
    def __str__(self):
        _fmt_param = ""
        for idx in range(len(self.parameters)):
            _fmt_param += self.parameters[idx]

            if  idx < len(self.parameters) - 1:
                _fmt_param += ", "
        return "function %s(%s){...}" % (self.name, _fmt_param)

    # ================ DUNDER METHODS|
    # ===============================|
    def call(self, _opt:CSToken, _arg_count:int):
        # core
        from cscriptvm.csvm import CSVM as VM

        if  _arg_count != self.paramcount:
            # = format string|
            _error = reformatError("expected parameter count %d, got %d" % (self.paramcount, _arg_count), _opt)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        _obj = VM.run(self.instructions)
        
        del VM
        return _obj



def reformatError(_message:str, _token:CSToken):
    """ By default, the entire error is string, not an exception.

        Prameters
        ---------
        _csexceptionobject : CSObject
        _token             : CSToken
    """
    _error = CSObject.new_string(
        ("[%s:%d:%d] CSError: %s" % (_token.fsrce, _token.yS, _token.xS, _message))
        + "\n" 
        + _token.trace
    )
    return _error


