from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst

# OK!!! | COMPILED | PASSED
class ArrayNode(ExpressionAst):
    """ Holds array node

        Parameters
        ----------
        _elements : CSToken
    """

    def __init__(self, _elements:tuple):
        super().__init__()
        self.elements = _elements
    
    def compile(self, _block:CodeBlock):
        # compile right most first!
        for node in self.elements[::-1]:
            _evaluated = node.evaluate()
            if  _evaluated:
                _block.push_constant(_evaluated)
            else:
                node.compile(_block)
        
        # array opcode
        _block.make_array(len(self.elements))


