from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken, CSAst


# OK!!! | COMPILED
class CallNode(ExpressionAst):
    """ Holds call node

        Parameters
        ----------
        _lefthand  : CSAst
        _arguments : tuple
        _opt       : CSToken
    """

    def __init__(self, _lefthand:CSAst, _arguments:tuple, _call_location:CSToken):
        super().__init__()
        self.lefthand  = _lefthand
        self.arguments = _arguments
        self.location  = _call_location
    
    def compile(self, _block:CodeBlock):
        # compile right most first!
        for node in self.arguments[::-1]:

            # value
            _evaluated = node.evaluate()
            if  _evaluated:
                _block.push_constant(_evaluated)
            else:
                node.compile(_block)
        
        # compile left
        self.lefthand.compile(_block)
        
        # call opcode
        _block.call(self.location, len(self.arguments))



