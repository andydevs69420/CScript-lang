from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


# OK!!! | COMPILED | PASSED
class BinaryExprNode(CSAst, Evaluator):
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
        
    def compile(self):
        _result = self.evaluate()
        if  _result:
            self.push_constant(_result)
            return
        
        # continue compilation

        # compile rhs
        self.rhs.compile()

        # compile lhs
        self.lhs.compile()

        # select by op
        if  self.opt.matches("^^"):
            self.binary_pow(self.opt)
        elif self.opt.matches("*"):
            self.binary_mul(self.opt)
        elif self.opt.matches("/"):
            self.binary_div(self.opt)
        elif self.opt.matches("%"):
            self.binary_mod(self.opt)
        elif self.opt.matches("+"):
            self.binary_add(self.opt)
        elif self.opt.matches("-"):
            self.binary_sub(self.opt)
        elif self.opt.matches("<<"):
            self.binary_lshift(self.opt)
        elif self.opt.matches(">>"):
            self.binary_rshift(self.opt)
        elif self.opt.matches("&"):
            self.binary_and(self.opt)
        elif self.opt.matches("^"):
            self.binary_xor(self.opt)
        elif self.opt.matches("|"):
            self.binary_or(self.opt)
        else:\
        raise NotImplementedError("invalid operator \"%s\"" % self.opt.token)
    
    def evaluate(self):
        _binary = self.evaluate_bin_op(self.opt, self.lhs, self.rhs)
        if  _binary:
            _binary.cleanLast()
        return _binary

