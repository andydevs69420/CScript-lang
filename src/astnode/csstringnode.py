from cstoken import CSToken
from csAst import CSAst

# object
from object.csobject import CSObject

# core
from cscriptvm.csevaluator import Evaluatable

# OK!!! | COMPILED | PASSED
class StringNode(CSAst, Evaluatable):
    """ Holds string node

        Parameters
        ----------
        _str : cstoken.CSToken
    """

    def __init__(self, _str:CSToken):
        super().__init__()
        self.string = _str
        
    def compile(self):
        self.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSObject.new_string(self.string.token)
