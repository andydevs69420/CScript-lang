from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken, CSAst

# OK!!! | COMPILED | PASSED
class UnaryExprNode(ExpressionAst):
    """ Holds unary expression node

        Parameters
        ----------
        _opt : cstoken.CSToken
        _rhs : CSAst
    """

    def __init__(self, _opt:CSToken, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.rhs = _rhs
    
    def compile(self, _block:CodeBlock):
        _result = self.evaluate()
        if  _result:
            _block.push_constant(_result)
            return
        
        # continue compilation

        # compile rhs
        self.rhs.compile(_block)

        # add op
        _block.unary_op(self.opt)
    
    def evaluate(self):
        return self.evaluate_unary_op(self.opt, self.rhs)

