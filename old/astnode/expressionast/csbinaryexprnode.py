from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst, CSToken, CSAst


# OK!!! | COMPILED | PASSED
class BinaryExprNode(ExpressionAst):
    """ Holds binary expression node

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
        _result = self.evaluate()
        if  _result:
            _block.push_constant(_result)
            return
        
        # continue compilation

        # compile rhs
        self.rhs.compile(_block)

        # compile lhs
        self.lhs.compile(_block)

        # select by op
        if  self.opt.matches("^^"):
            _block.binary_pow(self.opt)
        elif self.opt.matches("*"):
            _block.binary_mul(self.opt)
        elif self.opt.matches("/"):
            _block.binary_div(self.opt)
        elif self.opt.matches("%"):
            _block.binary_mod(self.opt)
        elif self.opt.matches("+"):
            _block.binary_add(self.opt)
        elif self.opt.matches("-"):
            _block.binary_sub(self.opt)
        elif self.opt.matches("<<"):
            _block.binary_lshift(self.opt)
        elif self.opt.matches(">>"):
            _block.binary_rshift(self.opt)
        elif self.opt.matches("&"):
            _block.binary_and(self.opt)
        elif self.opt.matches("^"):
            _block.binary_xor(self.opt)
        elif self.opt.matches("|"):
            _block.binary_or(self.opt)
        else:\
        raise NotImplementedError("invalid operator \"%s\"" % self.opt.token)
    
    def evaluate(self):
        return self.evaluate_bin_op(self.opt, self.lhs, self.rhs)

