


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
        self.put(CSFunction.KEY_NAME, _name)
        self.put(CSFunction.KEY_ARGC, _argc)
        self.put(CSFunction.KEY_CODE, _code)

        # debug:
        assert _name.offset != -69420, "not allocated!!!"
        assert _argc.offset != -69420, "not allocated!!!"
        assert _code.offset != -69420, "not allocated!!!"

    def __str__(self):
        """ Specify as native when printing in python
            to prevent confusions!
        """
        return "<CSFunction %s(){...}/>" % self.get(CSFunction.KEY_NAME).this
