
from cstoken import CSToken
from csobject import CSObject

# core
from cscriptvm.csvm import CSVirtualMachine as VM

class CSCallable(CSObject):

    def __init__(self, _name:str, _parameters:list, _instructions:list):
        super().__init__()
        self.name = _name
        self.parameters = _parameters
        self.instructions = _instructions
    
    #![bound:: toString]
    def toString(self):
        _fmt_param = ""
        for idx in range(len(self.parameters)):
            _fmt_param += self.parameters[idx]

            if  idx < len(self.parameters) - 1:
                _fmt_param += ", "
        return CSObject.new_string("function %s(%s){...}" % (self.name, _fmt_param))
    
    def get(self, _key: str):
        if  type(self) == CSCallable and _key == "this":
            return self
        return super().get(_key)

    # ================ DUNDER METHODS|
    # ===============================|
    def call(self, _opt:CSToken, _arg_count:int):
        return VM.run(self.instructions)
