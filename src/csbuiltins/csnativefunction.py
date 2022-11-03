


from .cstypes import CSTypes
from .base.csobject import CSObject


class CSNativeFunction(CSObject):
    """ Handles native function
    """
    KEY_NAME = "name"
    KEY_ARGC = "argc"

    def __init__(self, _name:CSObject, _argc:CSObject, _py_callable:callable):
        super().__init__()
        self.type = CSTypes.TYPE_CSNATIVEFUNCTION
        self.put(CSNativeFunction.KEY_NAME, _name)
        self.put(CSNativeFunction.KEY_ARGC, _argc)
        self.call = _py_callable
    
    def __str__(self):
        """ Specify as native when printing in python
            to prevent confusions!
        """
        return "<CSNativeFunction %s(){...}/>" % self.get(CSNativeFunction.KEY_NAME).this


