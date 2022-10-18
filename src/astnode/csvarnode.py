
from csAst import CSAst
from errortoken import show_error

# object
from object.csobject import CSObject

# core
from cscriptvm.cssymboltable import CSSymbolTable as ST
from cscriptvm.csvm import CSVirtualMachine as VM


# OK!!! | COMPILED | PASSED
class VarNode(CSAst):
    """ Holds var declairation

        Parameters
        ----------
        _assignments : tuple
    """
    def __init__(self, _assignments:tuple):
        super().__init__()
        self.assignments = _assignments
    
    def compile(self):
        for assignment in self.assignments:
            # compile value
            _val = assignment["val"]
            if  not _val:
                self.push_constant(CSObject.new_nulltype("null"))
            else:
                _val.compile()
            
            _var = assignment["var"]

            # ================= RECORDING PURPOSE|
            # ===================================|
            # check existence
            if  ST.islocal(_var.token):
                return show_error("variable \"%s\" is already defined" % _var.token, _var)
            
            # possible ok!
            _s = VM.makeSlot()

            # save var_name
            ST.insert(_var.token, _slot=_s, _global=True)

            # ============ MEMORY SETTING PURPOSE|
            # ===================================|
            # store name
            self.store_name(_var, _s)


