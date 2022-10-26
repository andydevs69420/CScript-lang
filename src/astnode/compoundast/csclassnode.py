from astnode.globalast.csAst import CSToken, CSAst, CSObject
from astnode.globalast.cscodeblock import CodeBlock


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
    
    def compile(self, _block:CodeBlock):
        _s = _block.newglobals()

        _block.symbtable.current.insert(self.name.token, _slot=_s, _global=True)

        # TODO: evaluate base name

        for each_member in self.member:
            # compile value
            each_member["value"].compile(_block)

            # push name
            _block.push_constant(CSObject.new_string(each_member["name"].token))
        
        # push class name
        _block.push_constant(CSObject.new_string(self.name.token))

        _block.make_class(len(self.member))

        _block.store_name(self.name, _s)

