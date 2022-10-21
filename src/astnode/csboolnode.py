from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable
from object import CSBoolean

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
        return CSBoolean(self.boolean.token)



