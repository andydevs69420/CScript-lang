from cstoken import CSToken
from csAst import CSAst



# OK!!! | COMPILED | PASSED
class SubscriptNode(CSAst):
    """ Holds subscription node

        Parameters
        ----------
        _lefthand : CSAst
        _expr     : CSAst
        _opt      : CSToken
    """

    def __init__(self, _lefthand:CSAst, _expr:CSAst, _opt:CSToken):
        super().__init__()
        self.lefthand   = _lefthand
        self.expression = _expr
        self.opt = _opt
    
    def compile(self):
        # compile left
        self.lefthand.compile()

        # compile expression
        self.expression.compile()

        # subscript opcode
        self.binary_subscript(self.opt)
    

    def assignTo(self):
        # compile left
        self.lefthand.compile()

        # compile expression
        self.expression.compile()

        # subscript opcode
        self.set_subscript(self.opt)



