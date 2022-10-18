


from cstoken import CSToken
from csspitcode import SpitsCode
from csblocknode import BlockNode
from errortoken import show_error

# object
from object.csobject import CSObject

# core
from cscriptvm.cssymboltable import CSSymbolTable as ST
from cscriptvm.csvm import CSVirtualMachine as VM


class FunctionNode(SpitsCode):
    """ Handles function node

        Parameters
        ----------
        _func_name  : CSToken
        _parameters : tuple
        _body       : BlockNode
    """

    def __init__(self, _func_name:CSToken, _parameters:tuple, _body:BlockNode):
        super().__init__()
        self.funcname   = _func_name
        self.parameters = _parameters
        self.body = _body
    
    def compile(self):
        self.newSet()
        
        # ================= RECORDING PURPOSE|
        # ===================================|
        # check existence
        if  ST.islocal(self.funcname.token):
            return show_error("variable \"%s\" is already defined" % self.funcname.token, self.funcname)
        
        _s = VM.makeSlot()
        _parameters:list[str] = []
        
        # save var_name
        ST.insert(self.funcname.token, _slot=_s, _global=True)

        ST.newScope()

        for tok in self.parameters[::-1]:
            _parameters.append(tok.token)

        self.body.compile()

        self.push_constant(CSObject.new_nulltype("null"))

        self.return_op()

        ST.endScope()

        _instructions = self.popSet()

        self.push_constant(CSObject.new_callable(self.funcname.token, _parameters[::-1], _instructions))

        # ============ MEMORY SETTING PURPOSE|
        # ===================================|
        # store name
        self.store_name(self.funcname, _s)

        return _instructions




    
    

