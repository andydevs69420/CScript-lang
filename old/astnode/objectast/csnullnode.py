from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken

# OK!!! | COMPILED | PASSED
class NullNode(ExpressionAst):
    """ Holds nulltype node

        Parameters
        ----------
        _null : CSToken
    """

    def __init__(self, _null:CSToken):
        super().__init__()
        self.nulltype = _null
        
    def compile(self, _block:CodeBlock):
        _block.push_constant(self.evaluate())
    
    def evaluate(self):
        return None
