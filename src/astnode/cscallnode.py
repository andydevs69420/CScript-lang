from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


# OK!!! | COMPILED
class CallNode(CSAst):
    """ Holds call node

        Parameters
        ----------
        _lefthand  : CSAst
        _arguments : tuple
        _opt       : CSToken
    """

    def __init__(self, _lefthand:CSAst, _arguments:tuple, _call_location:CSToken):
        super().__init__()
        self.lefthand  = _lefthand
        self.arguments = _arguments
        self.location  = _call_location
    
    def compile(self):
        # compile right most first!
        for node in self.arguments[::-1]:

            # value
            _evaluated = node.evaluate()
            if  _evaluated:
                self.push_constant(_evaluated)
            else:
                node.compile()
        
        # compile left
        self.lefthand.compile()
        
        # call opcode
        self.call(self.location, len(self.arguments))



