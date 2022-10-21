
from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


# OK!!! | COMPILED | PASSED
class TernaryNode(CSAst, Evaluator):
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
    
    def compile(self):
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return

        ## continue compilation ##
        self.condition.compile()

        self.pop_jump_if_false(...)
        _jump_t0 = self.peekLast()

        # compile true
        self.vtrue.compile()

        self.jump_to(...)
        _jump_t1 = self.peekLast()

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

        # compile false
        self.vfalse.compile()

        # set jump target 1
        _jump_t1.kwargs["target"] = self.getLine()

    
    def evaluate(self):
        return self.evaluate_ternary_op(self.condition, self.vtrue, self.vfalse)

