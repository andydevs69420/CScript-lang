


# .
from csbuiltins.cstypes import CSTypes
from .base.csobject import CSObject
from .code.csrawcode import csrawcode


class CSFunction(CSObject):
    """ Put every info as CSFunction attribute!
    """

    KEY_NAME = "name"
    KEY_ARGC = "argc"
    KEY_CODE = "code"

    def __init__(self, _name:CSObject, _argc:CSObject, _code:CSObject):
        super().__init__()
        self.type = CSTypes.TYPE_CSFUNCTION
        # thisArg
        self.put(CSFunction.KEY_NAME, _name)
        self.put(CSFunction.KEY_ARGC, _argc)
        self.put(CSFunction.KEY_CODE, _code)

    def __str__(self):
        """ Specify as native when printing in python
            to prevent confusions!
        """
        return "<CSFunction %s(){...}/>" % self.get(CSFunction.KEY_NAME).this
