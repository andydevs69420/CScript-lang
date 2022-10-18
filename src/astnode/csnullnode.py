from cstoken import CSToken
from csAst import CSAst

# object
from object.csobject import CSObject

# core
from cscriptvm.csevaluator import Evaluatable

# OK!!! | COMPILED | PASSED
class NullNode(CSAst, Evaluatable):
    """ Holds nulltype node

        Parameters
        ----------
        _null : CSToken
    """

    def __init__(self, _null:CSToken):
        super().__init__()
        self.nulltype = _null
        
    def compile(self):
        self.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSObject.new_nulltype(self.nulltype.token)
