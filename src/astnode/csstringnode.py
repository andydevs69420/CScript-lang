from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable
from object import CSString


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
        return CSString(self.string.token)
