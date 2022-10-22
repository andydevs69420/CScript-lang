from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken
from object import CSBoolean

# OK!!! | COMPILED | PASSED
class BoolNode(ExpressionAst):
    """ Holds boolean node

        Parameters
        ----------
        _bool : CSToken
    """

    def __init__(self, _bool:CSToken):
        super().__init__()
        self.boolean = _bool
        
    def compile(self, _block:CodeBlock):
        _block.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSBoolean(self.boolean.token)



