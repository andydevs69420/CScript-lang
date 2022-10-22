
from astnode.globalast.cscodeblock import CodeBlock


class ModuleNode(CodeBlock):
    """ Handles Module

        Parameters
        ----------
        _child_nodes : tuple
    """

    def __init__(self, _child_nodes:tuple):
        super().__init__()
        self.child_nodes = _child_nodes
    
    def compile(self):
        for node in self.child_nodes:
            node.compile(self)
        
        # module opcode
        self.make_module()

        # add default return
        self.return_op()

        return self.getInsntructions()