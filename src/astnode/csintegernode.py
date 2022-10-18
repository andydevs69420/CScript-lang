
from cstoken import CSToken
from csAst import CSAst

# object
from object.csobject import CSObject
from cscriptvm.csevaluator import Evaluatable

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
        
    def compile(self):
        self.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSObject.new_integer(int(self.integer.token))


