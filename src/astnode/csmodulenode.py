

from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable
from csspitcode import SpitsCode


class ModuleNode(SpitsCode):
    """ Handles Module

        Parameters
        ----------
        _child_nodes : tuple
    """

    def __init__(self, _child_nodes:tuple):
        super().__init__()
        self.child_nodes = _child_nodes
    
    def compile(self):
        self.newSet()

        ST.newScope()
        for node in self.child_nodes:
            node.compile()
        ST.endScope()
        
        # module opcode
        self.make_module()

        # add default return
        self.return_op()

        return self.popSet()