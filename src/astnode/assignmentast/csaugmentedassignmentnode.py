from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken, CSAst


# OK!!! | COMPILED | PASSED
class AugmentedAssignment(ExpressionAst):
    """ Holds augmented assignment

        Parameters
        ----------
        _opt : cstoken.CSToken
        _lhs : CSAst
        _rhs : CSAst
    """

    def __init__(self, _opt:CSToken, _lhs:CSAst, _rhs:CSAst):
        super().__init__()
        self.opt = _opt
        self.lhs = _lhs
        self.rhs = _rhs
    
    def compile(self, _block:CodeBlock):
        # compile rhs
        self.rhs.compile(_block)

        # compile lhs
        self.lhs.compile(_block)

        # compile by op
        if  self.opt.matches("^^="):
            _block.inplace_pow(self.opt)
        elif self.opt.matches("*="):
            _block.inplace_mul(self.opt)
        elif self.opt.matches("/="):
            _block.inplace_div(self.opt)
        elif self.opt.matches("%="):
            _block.inplace_mod(self.opt)
        elif self.opt.matches("+="):
            _block.inplace_add(self.opt)
        elif self.opt.matches("-="):
            _block.inplace_sub(self.opt)
        elif self.opt.matches("<<="):
            _block.inplace_lshift(self.opt)
        elif self.opt.matches(">>="):
            _block.inplace_rshift(self.opt)
        elif self.opt.matches("&="):
            _block.inplace_and(self.opt)
        elif self.opt.matches("^="):
            _block.inplace_xor(self.opt)
        elif self.opt.matches("|="):
            _block.inplace_or(self.opt)
        else:\
        raise NotImplementedError("invalid operator \"%s\"" % self.opt.token)

        # compile lhs
        self.lhs.assignTo(_block, self.opt)
