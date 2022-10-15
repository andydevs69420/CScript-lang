


from csobject import CSObject

class CSArray(CSObject):pass
class CSArray(CSObject):

    def __init__(self):
        super().__init__()
        self.size = 0
        self.elem = CSObject()
        self.put("length"  , self.size)
        self.put("elements", self.elem)
    
    # ![bound::push]
    def push(self, _csobject:CSObject):
        """ Push new item into array

            Returns
            -------
            CSObject
        """
        self.elem.put(str(self.size), _csobject)
        self.size += 1
    
        # default return
        return CSObject.new_nulltype("null")
    
    # ![bound::pop]
    def pop(self, _csobject:CSObject):
        """ Pop item into array

            Returns
            -------
            CSObject
        """
    
    # ![bound::toString]
    def toString(self):
        _elem = ""
        for idx in range(self.size):
            _elem += str(self.elem.get(str(idx)))

            if  idx < (self.size - 1):
                _elem += ", "
        
        # return formated string
        return CSObject.new_string("[" + _elem + "]")

    def reBuild(self):
        """ Rebuilds array when pop|del is called
        """
        ...

    @staticmethod
    def fromArray(_array:CSArray):
        """ Creates a new array from existing array

            Returns
            -------
            CSArray
        """