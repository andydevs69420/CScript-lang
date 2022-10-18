
from csAst import CSAst
from errortoken import show_error

# object
from object.csobject import CSObject


class LetNode(CSAst):
    """ Holds let declairation

        Parameters
        ----------
        _assignments : tuple
    """

    def __init__(self, _assignments:tuple):
        super().__init__()
        self.assignments = _assignments
    
    def compile(self):
        for assignment in self.assignments:
            # compile value
            if  not assignment["val"]:
                self.push_constant(CSObject.new_nulltype("null"))
            else:
                assignment["val"].compile()
            
            # push name
            self.push_constant(CSObject.new_string(assignment["var"].token))


