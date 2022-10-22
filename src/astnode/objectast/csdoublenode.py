from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken
from object import CSDouble


# OK!!! | COMPILED | PASSED
class DoubleNode(ExpressionAst):
    """ Holds double node

        Parameters
        ----------
        _str : CSToken
    """

    def __init__(self, _double:CSToken):
        super().__init__()
        self.double = _double
        
    def compile(self, _block:CodeBlock):
        _block.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSDouble(self.double.token)

