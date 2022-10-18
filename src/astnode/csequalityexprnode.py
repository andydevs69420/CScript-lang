

from cstoken import CSToken
from csAst import CSAst
from cscompareexprnode import CompareExprNode


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

    def compile(self):
        return super().compile()
    
    def evaluate(self):
        return super().evaluate()



