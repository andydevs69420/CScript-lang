
from cstoken import CSToken
from csAst import CSAst



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
    
    def compile(self):
        return super().compile()
