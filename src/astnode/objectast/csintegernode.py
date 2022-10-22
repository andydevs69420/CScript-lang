from astnode.globalast.csAst import CSToken, CSAst, Evaluatable
from astnode.globalast.cscodeblock import CodeBlock
from object import CSInteger


# OK!!! | COMPILED | PASSED 
class IntegerNode(CSAst, Evaluatable):
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

