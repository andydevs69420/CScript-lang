from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

class ReturnNode(CSAst):
    """ Handles return statement

        Parameters
        ----------
    """

    def __init__(self, _expr:CSAst|None):
        super().__init__()
        self.expression = _expr
    
    def compile(self):
        if  self.expression:
            # compile expr
            self.expression.compile()
        else:
            self.push_constant(CSObject.new_nulltype("null"))

        # compile return
        self.return_op()

