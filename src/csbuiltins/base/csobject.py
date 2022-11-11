
from .hashmap import HashMap

# for typing
class CSObject(HashMap):pass
class CSObject(HashMap):
    """ Represents Object in CScript
    """
    
    def __init__(self):
        super().__init__()
        # ======== memory flags|
        # =====================|
        self.offset = -69420
        self.marked = False

        self.type = type(self).__name__

        self.hidden = ["__proto__", "qualname"]

    def __str__(self):
        return self.type +":"+ super().__str__()
    



