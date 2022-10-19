from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

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
        _integer = CSObject.new_integer(int(self.integer.token))
        _integer.cleanLast()
        return _integer


