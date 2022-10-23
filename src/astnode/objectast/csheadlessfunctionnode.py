from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst
from astnode.compoundast.csblocknode import BlockNode
from astnode.globalast.csAst import CSObject, show_error



class HeadlessFunctionNode(CodeBlock, ExpressionAst):
    """ Handles function node

        Parameters
        ----------
        _parameters : tuple
        _body       : BlockNode
    """

    def __init__(self, _parameters:tuple, _body:BlockNode):
        super().__init__()
        self.parameters = _parameters
        self.body = _body
    
    def compile(self, _block:CodeBlock):
        # set parent of newly created node
        self.symbtable.current.setParent(_block.symbtable.current)
        
        _parameters:list[str] = []

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
        _block.push_constant(CSObject.new_callable("headless", _parameters, _instructions, _allocate=False))

        return _instructions




    
    

