from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable
from object import CSNullType

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
        return CSNullType()
