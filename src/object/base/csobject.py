
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

    



