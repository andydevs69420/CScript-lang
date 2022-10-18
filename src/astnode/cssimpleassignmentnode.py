


from cstoken import CSToken
from csAst import CSAst
from errortoken import show_error


class SimpleAssignment(CSAst):
    """ Holds simple assignment

        Parameters
        ----------
        _opt : CSToken
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
        self.lhs.assignTo()