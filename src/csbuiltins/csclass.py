

from csbuiltins.base.csobject import CSObject


class CSClass(CSObject):

    KEY_NAME = "name"

    def __init__(self, _name:CSObject):
        super().__init__()
        self.put(CSClass.KEY_NAME, _name)
    


