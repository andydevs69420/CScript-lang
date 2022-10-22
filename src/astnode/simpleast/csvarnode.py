from astnode.globalast.csAst import CSAst, CSObject, show_error, VM
from astnode.globalast.cscodeblock import CodeBlock

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
    
    def compile(self, _block:CodeBlock):
        for assignment in self.assignments:
            # compile value
            _val = assignment["val"]
            if  not _val:
                _block.push_constant(CSObject.new_nulltype())
            else:
                _val.compile(_block)
            
            _var = assignment["var"]

            # ================= RECORDING PURPOSE|
            # ===================================|
            # check existence
            if  _block.symbtable.globaltable.existslocally(_var.token):
                return show_error("variable \"%s\" is already defined" % _var.token, _var)
            
            # possible ok!
            _s = _block.newglobals()

            # save var_name
            _block.symbtable.globaltable.insert(_var.token, _slot=_s, _global=True)

            # ============ MEMORY SETTING PURPOSE|
            # ===================================|
            # store name
            _block.store_name(_var, _s)


