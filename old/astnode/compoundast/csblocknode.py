from astnode.globalast.csAst import CSToken, CSAst, ST
from astnode.globalast.cscodeblock import CodeBlock


# OK!!! | COMPILED | PASSED
class BlockNode(CSAst):
    """ Holds block of statement

        Parameters
        ----------
        _statements : tuple
    """

    def __init__(self, _statements:tuple):
        super().__init__()
        self.statements = _statements
    
    def compile(self, _block:CodeBlock):
        _block.symbtable.newScope()
        for stmnt in self.statements:
            stmnt.compile(_block)
        _block.symbtable.endScope()

