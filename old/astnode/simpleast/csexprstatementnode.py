from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock

# OK!!! | COMPILED | PASSED
class ExprStmntNode(CSAst):
    """ Handles expression statement

        Parameters
        ----------
        _expr : CSAst
    """


    def __init__(self, _expr:CSAst):
        super().__init__()
        self.expr = _expr
    
    def compile(self, _block:CodeBlock):
        # compile expr
        self.expr.compile(_block)

        # pop code
        _block.pop_top()
