from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


# OK!!! | COMPILED | PASSED
class PrintNode(CSAst):
    """ Handles print statement

        Parameters
        ----------
        _expr_list : list
    """

    def __init__(self, _expr_list:tuple):
        super().__init__()
        self.expressions = _expr_list

    
    def compile(self):
        # compile right most
        for node in self.expressions[::-1]:
            node.compile()
        
        # print opcode
        self.print_object(len(self.expressions))

