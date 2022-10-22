


from astnode.globalast.csAst import CSToken, show_error, CSObject, VM
from astnode.compoundast.csblocknode import BlockNode
from astnode.globalast.cscodeblock import CodeBlock



class FunctionNode(CodeBlock):
    """ Handles function node

        Parameters
        ----------
        _func_name  : CSToken
        _parameters : tuple
        _body       : BlockNode
    """

    def __init__(self, _func_name:CSToken, _parameters:tuple, _body:BlockNode):
        super().__init__()
        self.funcname   = _func_name
        self.parameters = _parameters
        self.body = _body
    
    def compile(self, _block:CodeBlock):
        # set parent of newly created node
        self.symbtable.current.setParent(_block.symbtable.current)

        # ================= RECORDING PURPOSE|
        # ===================================|
        # check existence
        if  _block.symbtable.globaltable.existslocally(self.funcname.token):
            return show_error("variable \"%s\" is already defined" % self.funcname.token, self.funcname)
        
        _s = _block.newglobals()
        _parameters:list[str] = []
        
        # save var_name
        _block.symbtable.globaltable.insert(self.funcname.token, _slot=_s, _global=True)

        for tok in self.parameters:
            _parameters.append(tok.token)
            # store local opcode
            _l = self.newlocals()

            # ================= RECORDING PURPOSE|
            # ===================================|
            # check existence
            if  self.symbtable.current.existslocally(tok.token):
                return show_error("parameter \"%s\" is already defined" % tok.token, tok)
            
            # save param
            self.symbtable.current.insert(tok.token, _slot=_l, _global=False)

            # ============ MEMORY SETTING PURPOSE|
            # ===================================|
            # store name
            self.store_local(tok, _l)

        # iter node
        for each_node in self.body:
            each_node.compile(self)

        self.push_constant(CSObject.new_nulltype())

        self.return_op()

        _instructions = self.getInsntructions()
        # for i in _instructions:
        #     print(i)

        # push function to block
        _block.push_constant(CSObject.new_callable(self.funcname.token, _parameters, _instructions))

        # ============ MEMORY SETTING PURPOSE|
        # ===================================|
        # store name
        _block.store_name(self.funcname, _s)




    
    

