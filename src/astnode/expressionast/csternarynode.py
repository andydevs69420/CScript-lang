from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken, CSAst


# OK!!! | COMPILED | PASSED
class TernaryNode(ExpressionAst):
    """ Holds ternary node

        Parameters
        ----------
        _condition : CSAst
        _true      : CSAst
        _false     : CSAst
    """

    def __init__(self, _condition:CSAst, _true:CSAst, _false:CSAst):
        super().__init__()
        self.condition = _condition
        self.vtrue  = _true
        self.vfalse = _false
    
    def compile(self, _block:CodeBlock):
        _result = self.evaluate()
        if  _result:
            _block.push_constant(_result)
            return

        ## continue compilation ##
        self.condition.compile(_block)

        _block.pop_jump_if_false(...)
        _jump_t0 = _block.peekLast()

        # compile true
        self.vtrue.compile(_block)

        _block.jump_to(...)
        _jump_t1 = _block.peekLast()

        # set jump target 0
        _jump_t0.kwargs["target"] = _block.getLine()

        # compile false
        self.vfalse.compile(_block)

        # set jump target 1
        _jump_t1.kwargs["target"] = _block.getLine()

    
    def evaluate(self):
        return self.evaluate_ternary_op(self.condition, self.vtrue, self.vfalse)

