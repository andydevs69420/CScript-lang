from cstoken import CSToken
from csAst import CSAst

# object
from object.csobject import CSObject


# OK!!! | COMPILED | PASSED
class DoubleNode(CSAst):
    """ Holds double node

        Parameters
        ----------
        _str : CSToken
    """

    def __init__(self, _double:CSToken):
        super().__init__()
        self.double = _double
        
    def compile(self):
        self.push_constant(self.evaluate())
    
    def evaluate(self):
        return CSObject.new_double(float(self.double.token))

