

from cstoken import CSToken
from csAst import CSAst
from cscompareexprnode import CompareExprNode


# OK!!! | COMPILED | SHORT CIRCUITING | PASSED
class LogicalExprNode(CompareExprNode):
    """ Holds logical expression|jump|shortcircuit

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    def __init__(self, _opt: CSToken, _lhs: CSAst, _rhs: CSAst):
        super().__init__(_opt, _lhs, _rhs)
    
    def compile(self):
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return

        # continue compilation
        """ Compile lhs first when 
            short-circuiting
        """

        # compile lhs
        self.lhs.compile()

        _jump_t0 = None

        if  self.opt.matches("&&"):
            # logical and
            self.jump_if_false_or_pop(...)
            _jump_t0 = self.peekLast()
        else:
            # logical or
            self.jump_if_true_or_pop(...)
            _jump_t0 = self.peekLast()

        # compile rhs
        self.rhs.compile()

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

    def isOverloading(self):
        return True

    def evaluate(self):
        return super().evaluate()


