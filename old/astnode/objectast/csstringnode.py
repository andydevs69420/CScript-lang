from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken


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
        return str(self.string.token)
