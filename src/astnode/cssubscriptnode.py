from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

# OK!!! | COMPILED | PASSED
class SubscriptNode(CSAst):
    """ Holds subscription node

        Parameters
        ----------
        _lefthand : CSAst
        _expr     : CSAst
        _opt      : CSToken
    """

    def __init__(self, _lefthand:CSAst, _expr:CSAst, _subscript_location:CSToken):
        super().__init__()
        self.lefthand   = _lefthand
        self.expression = _expr
        self.subscript_location = _subscript_location
    
    def compile(self):
        # compile left
        self.lefthand.compile()

        # compile expression
        self.expression.compile()

        # subscript opcode
        self.binary_subscript(self.subscript_location)
    

    def assignTo(self):
        # compile left
        self.lefthand.compile()

        # compile expression
        self.expression.compile()

        # subscript opcode
        self.set_subscript(self.subscript_location)



