from astnode.globalast.csAst import CSToken
from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst
from object import CSInteger


# OK!!! | COMPILED | PASSED 
class IntegerNode(ExpressionAst):
    """ Holds integer node

        Parameters
        ----------
        _str : CSToken
    """

    def __init__(self, _int:CSToken):
        super().__init__()
        self.integer = _int
        
    def compile(self, _block:CodeBlock):
        _block.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSInteger(int(self.integer.token))


