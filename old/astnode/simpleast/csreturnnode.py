from astnode.globalast.csAst import CSAst, CSObject
from astnode.globalast.cscodeblock import CodeBlock


class ReturnNode(CSAst):
    """ Handles return statement

        Parameters
        ----------
    """

    def __init__(self, _expr:CSAst|None):
        super().__init__()
        self.expression = _expr
    
    def compile(self, _block:CodeBlock):
        if  self.expression:
            # compile expr
            self.expression.compile(_block)
        else:
            _block.push_constant(CSObject.new_nulltype())

        # compile return
        _block.return_op()

