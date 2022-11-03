


from base.csobject import CSObject

class csrawcode(CSObject):
    """ csrawcode class

        csrawcode is executable,
            it can be called !
        let name and instructions 
            be native in python.
            do not include as attribute!!!
    """

    def __init__(self, _name:str, _code:tuple):
        super().__init__()
        self.name = _name
        self.code = _code
    
    def __str__(self):
        """ Specify as native when printing in python
            to prevent confusions!
        """
        return "[NATIVE: csrawcode :for='%s' at %s]" % (self.name, hex(id(self)))

    def __iter__(self):
        return self.code.__iter__()
    
    def __len__(self):
        return len(self.code)
