
from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

from csspitcode import SpitsCode
from csblocknode import BlockNode



class HeadlessFunctionNode(SpitsCode):
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
    
    def compile(self):
        self.newSet()
        
        _parameters:list[str] = []
        ST.newScope()

        for tok in self.parameters:
            _parameters.append(tok.token)
            # store local opcode
            _l = ST.countLocal()

            # ================= RECORDING PURPOSE|
            # ===================================|
            # check existence
            if  ST.islocal(tok.token):
                return show_error("parameter \"%s\" is already defined" % tok.token, tok)
            
            # save param
            ST.insert(tok.token, _slot=_l, _global=False)

            # ============ MEMORY SETTING PURPOSE|
            # ===================================|
            # store name
            self.store_local(tok, _l)

        self.body.compile()

        self.push_constant(CSObject.new_nulltype("null"))

        self.return_op()

        ST.endScope()

        _instructions = self.popSet()

        self.push_constant(CSObject.new_callable("headless", _parameters, _instructions))
        return _instructions




    
    

