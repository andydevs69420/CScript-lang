

from astnode.expressionast.cscompareexprnode import CSToken, CSAst, CompareExprNode
from astnode.globalast.cscodeblock import CodeBlock


# OK!!! | COMPILED | PASSED
class EqualityExprNode(CompareExprNode):
    """ Holds equality expression|jump

        Parameters
        ----------
        _opt : CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    def __init__(self, _opt: CSToken, _lhs: CSAst, _rhs: CSAst):
        super().__init__(_opt, _lhs, _rhs)

    def compile(self, _block:CodeBlock):
        return super().compile(_block)
    
    def evaluate(self):
        return super().evaluate()



