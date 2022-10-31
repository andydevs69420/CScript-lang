from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock


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

    
    def compile(self, _block:CodeBlock):
        # compile right most
        for node in self.expressions[::-1]:
            node.compile(_block)
        
        # print opcode
        _block.print_object(len(self.expressions))

