from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken, CSAst

class SimpleAssignment(ExpressionAst):
    """ Holds simple assignment

        Parameters
        ----------
        _opt : CSToken
        _lhs : CSAst
        _rhs : CSAst
    """
    
    def __init__(self, _opt:CSToken, _lhs:CSAst, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.lhs = _lhs
        self.rhs = _rhs
    
    def compile(self, _block:CodeBlock):
        self.rhs.compile(_block)

        # compile lhs
        self.lhs.assignTo(_block, self.opt)