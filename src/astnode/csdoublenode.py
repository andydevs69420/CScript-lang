from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


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
        _double = CSObject.new_double(float(self.double.token))
        _double.cleanLast()
        return _double

