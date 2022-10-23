from csobject import CSToken, CSObject, ThrowError


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
        self.put("name"      , CSObject.new_string (_name       ))
        self.put("paramCount", CSObject.new_integer(_param_count))
        self.put("parameters", CSObject.new_array_from_PyList(_parameters))
        self.instructions = _instructions
    
    # ============ PYTHON|
    # ===================|
    
    def get(self, _key: str):
        if  type(self) == CSCallable and _key == "this":
            return self
        return super().get(_key)
    
    def isPointer(self):
        return True
    
    def __str__(self):
        _fmt_param = ""
        for idx in range(self.get("parameters").get("length").get("this")):
            _fmt_param += self.get("parameters").get("elements").get(str(idx)).__str__()

            if  idx < self.get("parameters").get("length").get("this") - 1:
                _fmt_param += ", "
        return "function %s(%s){...}" % (self.get("name"), _fmt_param)

    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribte
    def call(self, _opt:CSToken, _arg_count:int):
        # core
        from cscriptvm.csvm import CSVM as VM

        if  _arg_count != self.get("paramCount").get("this"):
            # = format string|
            _error = CSObject.new_type_error("expected parameter count %d, got %d" % (self.get("paramCount").get("this"), _arg_count), _opt)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        _obj = VM.run(self.instructions)
        
        del VM
        return _obj
