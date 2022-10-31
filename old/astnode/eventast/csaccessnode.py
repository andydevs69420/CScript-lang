
from astnode.globalast.csAst import CSToken, CSAst
from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst

# OK!!! | COMPILED | PASSED
class AccessNode(ExpressionAst):
    """ Holds member access node

        Parameters
        ----------
        _lefthand  : CSAst
        _attribute : CSToken
    """

    def __init__(self, _lefthand:CSAst, _attribute:CSToken):
        super().__init__()
        self.lefthand  = _lefthand
        self.attribute = _attribute
    
    def compile(self, _block:CodeBlock):
        # compile lhs
        self.lefthand.compile(_block)

        # attrib
        _block.get_attrib(self.attribute)
    
    def assignTo(self, _block:CodeBlock, _opt:CSToken):
        # compile lhs
        self.lefthand.compile(_block)

        # attrib
        _block.set_attrib(self.attribute)
        

    