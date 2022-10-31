
from astnode.globalast.csAst import CSToken, CSAst
from astnode.globalast.cscodeblock import CodeBlock
from errortoken import show_error


# TODO: implement
class AllocDeallocNode(CSAst):
    """ Holds allocate and deallocate expression node

        Parameters
        ----------
        _opt : cstoken.CSToken
        _rhs : CSAst
    """

    def __init__(self, _opt:CSToken, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.rhs = _rhs
    
    def compile(self, _block:CodeBlock):
        if  self.opt.matches("del"):
            return
        elif self.opt.matches("new"):
            return self.allocation(_block)
    
    def allocation(self, _block:CodeBlock):
        # compile
        self.rhs.compile(_block)

        _block.unary_op(self.opt)
