from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


# OK!!! | COMPILED | PASSED
class ArrayNode(CSAst):
    """ Holds array node

        Parameters
        ----------
        _elements : CSToken
    """

    def __init__(self, _elements:tuple):
        super().__init__()
        self.elements = _elements
    
    def compile(self):
        # compile right most first!
        for node in self.elements[::-1]:
            _evaluated = node.evaluate()
            if  _evaluated:
                self.push_constant(_evaluated)
            else:
                node.compile()
        
        # array opcode
        self.make_array(len(self.elements))


