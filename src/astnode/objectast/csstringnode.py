from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken
from object import CSString



# OK!!! | COMPILED | PASSED
class StringNode(ExpressionAst):
    """ Holds string node

        Parameters
        ----------
        _str : cstoken.CSToken
    """

    def __init__(self, _str:CSToken):
        super().__init__()
        self.string = _str
        
    def compile(self, _block:CodeBlock):
        _block.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSString(self.string.token)
