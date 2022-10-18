from cstoken import CSToken
from csAst import CSAst



# OK!!! | COMPILED | PASSED
class AccessNode(CSAst):
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
    
    def compile(self):
        # compile lhs
        self.lefthand.compile()

        # attrib
        self.get_attrib(self.attribute)
    
    def isMemberAssignable(self):
        return True
    
    def assignTo(self):
        # compile lhs
        self.lefthand.compile()

        # attrib
        self.set_attrib(self.attribute)
        

    