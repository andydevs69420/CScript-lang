


from base.csobject import CSObject


class NonPointer(CSObject):
    """ To group
    """
    
    THIS= "this"

    def __init__(self):
        super().__init__()
        self.initializeBound()
    
    # ======================== PYTHON|
    # ===============================|

    def all(self):
        return []
    
    def python(self):
        return self.thiso.get(NonPointer.THIS)