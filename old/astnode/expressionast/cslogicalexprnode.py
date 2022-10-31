
from astnode.expressionast.cscompareexprnode import CSToken, CSAst, CompareExprNode
from astnode.globalast.cscodeblock import CodeBlock


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
    
    def compile(self, _block:CodeBlock):
        _result = self.evaluate()
        if  _result:
            _block.push_constant(_result)
            return

        # continue compilation
        """ Compile lhs first when 
            short-circuiting
        """

        # compile lhs
        self.lhs.compile(_block)

        _jump_t0 = None

        if  self.opt.matches("&&"):
            # logical and
            _block.jump_if_false_or_pop(...)
            _jump_t0 = _block.peekLast()
        else:
            # logical or
            _block.jump_if_true_or_pop(...)
            _jump_t0 = _block.peekLast()

        # compile rhs
        self.rhs.compile(_block)

        # set jump target 0
        _jump_t0.kwargs["target"] = _block.getLine()

    def islogical(self):
        return True

    def evaluate(self):
        return super().evaluate()


