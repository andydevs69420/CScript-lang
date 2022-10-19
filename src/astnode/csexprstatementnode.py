from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

# OK!!! | COMPILED | PASSED
class ExprStmntNode(CSAst):
    """ Handles expression statement

        Parameters
        ----------
        _expr : CSAst
    """


    def __init__(self, _expr:CSAst):
        super().__init__()
        self.expr = _expr
    
    def compile(self):
        # compile expr
        self.expr.compile()

        # pop code
        self.pop_top()
