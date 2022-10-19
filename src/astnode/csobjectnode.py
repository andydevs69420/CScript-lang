from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

# OK!!! | COMPILED | PASSED
class ObjectNode(CSAst):
    """ Holds object node

        Parameters
        ----------
        _elements : tuple
    """

    def __init__(self, _elements:tuple):
        super().__init__()
        self.elements = _elements

    def compile(self):
        # compile right most first!
        for node in self.elements[::-1]:

            # value
            _evaluated = node["val"].evaluate()
            if  _evaluated:
                self.push_constant(_evaluated)
            else:
                node["val"].compile()
            
            # key|attrib
            self.push_constant(CSObject.new_string(node["key"].token))

        # object opcode
        self.make_object(len(self.elements))
