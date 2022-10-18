
from cstoken import CSToken
from csAst import CSAst

# object
from object.csobject import CSObject


class ClassNode(CSAst):
    """ Handles class node

        Parameters
        ----------
        _name : CSToken
        _base : CSToken
        _member : tuple
    """

    def __init__(self, _name:CSToken, _base:CSToken|None, _member:tuple):
        super().__init__()
        self.name   = _name
        self.base   = _base
        self.member = _member
    
    def compile(self):
        # push class name
        self.push_constant(CSObject.new_string(self.name.token))

        # TODO: evaluate base name

        for each_member in self.member:
            # compile value
            each_member["value"].compile()

            # push name
            self.push_constant(CSObject.new_string(each_member["name"].token))
        
        self.make_class(len(self.member))

