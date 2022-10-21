from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


# OK!!! | COMPILED | PASSED
class CompareExprNode(CSAst, Evaluator):
    """ Holds comparison expression node

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    def __init__(self, _opt:CSToken, _lhs:CSAst, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.lhs = _lhs
        self.rhs = _rhs
        
    def compile(self):
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return

        # continue compilation

        # compile rhs
        self.rhs.compile()

        # compile lhs
        self.lhs.compile()

        # add op
        self.compare_op(self.opt)

    def evaluate(self):
        return self.evaluate_comp_op(self.opt, self.lhs, self.rhs)


