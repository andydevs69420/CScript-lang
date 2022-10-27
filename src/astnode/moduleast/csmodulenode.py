
from astnode.globalast.cscodeblock import CodeBlock
from base.csobject import CSObject


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
        
        for each_key in list(self.symbtable.current.symbols.keys())[::-1]:
            _info = self.symbtable.current.symbols[each_key]

            # fetch current value
            self.push_name(_info["_token"], _info["_slot"])

            # prepare name
            self.push_constant(CSObject.new_string(each_key))


        # module opcode
        self.make_module(self.getglobals())

        # add default return
        self.return_op()
    
        return self.getInsntructions()