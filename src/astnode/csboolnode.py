
from cstoken import CSToken
from csAst import CSAst

# object
from object.csobject import CSObject

# core
from cscriptvm.csevaluator import Evaluatable


# OK!!! | COMPILED | PASSED
class BoolNode(CSAst, Evaluatable):
    """ Holds boolean node

        Parameters
        ----------
        _bool : CSToken
    """

    def __init__(self, _bool:CSToken):
        super().__init__()
        self.boolean = _bool
        
    def compile(self):
        self.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSObject.new_boolean(self.boolean.token)



