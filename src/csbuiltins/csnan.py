


from csbuiltins.cstypes import CSTypes
from .base.csobject import CSObject


class CSNaN(CSObject):
    """ Hanldes Not A Number type
    """

    def __init__(self):
        super().__init__()
        self.type = CSTypes.TYPE_CSNANTYPE
        self.this = None
    
    def __str__(self):
        return "NaN"