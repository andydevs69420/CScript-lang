from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

# OK!!! | COMPILED | PASSED
class UnaryExprNode(CSAst, Evaluator):
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
    
    def compile(self):
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return
        
        # continue compilation

        # compile rhs
        self.rhs.compile()

        # add op
        self.unary_op(self.opt)
    
    def evaluate(self):
        return self.evaluate_unary_op(self.opt, self.rhs)

