
from cstoken import CSToken
from csAst import CSAst
from errortoken import show_error


# OK!!! | COMPILED | PASSED
class AugmentedAssignment(CSAst):
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
        # make sure left hand is assignable
        if  not (self.lhs.isAssignable() or self.lhs.isMemberAssignable()):
            return show_error("invalid left-hand expression", self.opt)
    
    def compile(self):
        # compile rhs
        self.rhs.compile()

        # compile lhs
        self.lhs.compile()

        # compile by op
        if  self.opt.matches("^^="):
            self.inplace_pow(self.opt)
        elif self.opt.matches("*="):
            self.inplace_mul(self.opt)
        elif self.opt.matches("/="):
            self.inplace_div(self.opt)
        elif self.opt.matches("%="):
            self.inplace_mod(self.opt)
        elif self.opt.matches("+="):
            self.inplace_add(self.opt)
        elif self.opt.matches("-="):
            self.inplace_sub(self.opt)
        elif self.opt.matches("<<="):
            self.inplace_lshift(self.opt)
        elif self.opt.matches(">>="):
            self.inplace_rshift(self.opt)
        elif self.opt.matches("&="):
            self.inplace_and(self.opt)
        elif self.opt.matches("^="):
            self.inplace_xor(self.opt)
        elif self.opt.matches("|="):
            self.inplace_or(self.opt)
        else:\
        raise NotImplementedError("invalid operator \"%s\"" % self.opt.token)

        # compile lhs
        self.lhs.assignTo()
