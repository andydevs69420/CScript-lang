
from csAst import CSAst

# core
from cscriptvm.csvm import CSVirtualMachine as VM
from cscriptvm.cssymboltable import CSSymbolTable as ST

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
    
    def compile(self):
        ST.newScope()
        for stmnt in self.statements:
            stmnt.compile()
        ST.endScope()

