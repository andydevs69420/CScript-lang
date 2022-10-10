


from csobject import CSObject

class CSArray(CSObject):pass
class CSArray(CSObject):

    def __init__(self):
        super().__init__()
        self.put("size"    , 0)
        self.put("elements", CSObject())
    
    # ![bound::push]
    def push(self, _csobject:CSObject):
        """ Push new item into array

            Returns
            -------
            CSObject
        """
    
    # ![bound::pop]
    def pop(self, _csobject:CSObject):
        """ Pop item into array

            Returns
            -------
            CSObject
        """
    
    # ![bound::toString]
    def toString(self):pass


    @staticmethod
    def fromArray(_array:CSArray):
        """ Creates a new array from existing array

            Returns
            -------
            CSArray
        """