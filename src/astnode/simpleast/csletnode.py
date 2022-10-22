
from astnode.globalast.csAst import CSAst, show_error, CSObject
from astnode.globalast.cscodeblock import CodeBlock

class LetNode(CSAst):
    """ Holds let declairation

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
            if  not assignment["val"]:
                # unstable | not appropriate
                _block.push_constant(CSObject.new_nulltype())
            else:
                assignment["val"].compile(_block)
            

            _var = assignment["var"]

            # ================= RECORDING PURPOSE|
            # ===================================|
            # check existence
            if  _block.symbtable.current.existslocally(_var.token):
                return show_error("local variable \"%s\" is already defined" % _var.token, _var)
            
            # possible ok!
            _s = _block.newlocals()

            # save var_name
            _block.symbtable.current.insert(_var.token, _slot=_s, _global=False)

            # ============ MEMORY SETTING PURPOSE|
            # ===================================|
            # store name
            _block.store_local(_var, _s)


