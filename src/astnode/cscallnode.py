
from cstoken import CSToken
from csAst import CSAst

# OK!!! | COMPILED
class CallNode(CSAst):
    """ Holds call node

        Parameters
        ----------
        _lefthand  : CSAst
        _arguments : tuple
        _opt       : CSToken
    """

    def __init__(self, _lefthand:CSAst, _arguments:tuple, _opt:CSToken):
        super().__init__()
        self.lefthand  = _lefthand
        self.arguments = _arguments
        self.opt = _opt
    
    def compile(self):
        # compile left
        self.lefthand.compile()

        # compile right most first!
        for node in self.arguments[::-1]:

            # value
            _evaluated = node.evaluate()
            if  _evaluated:
                self.push_constant(_evaluated)
            else:
                node.compile()
        
        # call opcode
        self.call(self.opt, len(self.arguments))



