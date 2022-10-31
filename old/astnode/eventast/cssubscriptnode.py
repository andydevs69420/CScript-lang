from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSAst, CSToken

# OK!!! | COMPILED | PASSED
class SubscriptNode(ExpressionAst):
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
    
    def compile(self, _block:CodeBlock):
        # compile left
        self.lefthand.compile(_block)

        # compile expression
        self.expression.compile(_block)

        # subscript opcode
        _block.binary_subscript(self.subscript_location)
    

    def assignTo(self, _block:CodeBlock, _opt:CSToken):
        # compile lhs
        self.lefthand.compile(_block)

        # compile expression
        self.expression.compile(_block)

        # subscript opcode
        _block.set_subscript(self.subscript_location)


