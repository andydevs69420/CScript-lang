


from csbuiltins.cstypes import CSTypes
from csbuiltins.base.csobject import CSObject


class CSMethod(CSObject):
    """ Wraps a function to method
    """

    KEY_THIS ="this"
    KEY_NAME ="name"
    KEY_ARGC ="argc"
    KEY_CODE ="code"

    def __init__(self, _owner:CSObject, _method:CSObject):
        super().__init__()
        self.type = CSTypes.TYPE_CSMETHOD
        self.meth = _method.type
        self.put(CSMethod.KEY_THIS, _owner )
        self.put(CSMethod.KEY_NAME, _method.get(CSMethod.KEY_NAME))
        self.put(CSMethod.KEY_ARGC, _method.get(CSMethod.KEY_ARGC))

        if  _method.type == CSTypes.TYPE_CSNATIVEFUNCTION:
            self.call = _method.call
        else:
            self.put(CSMethod.KEY_CODE, _method.get(CSMethod.KEY_CODE))
        
        # debug:
        # assert _owner.offset != -69420, "not allocated!!!"
        
    
    def __str__(self):
        return "<CSMethod %s />" % self.get(CSMethod.KEY_NAME).__str__()


