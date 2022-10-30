



from base.csobject import CSObject

class CSIO(CSObject):
    def __init__(self):
        super().__init__()
        self.initializeBound()

    
    def initializeBound(self):
        super().initializeBound()

        # ============ WRITE|
        # ==================|
        self.proto.put("write", CSObject.new_bound_method("write", self.write, 1))
        self.proto.put("read" , CSObject.new_bound_method("read" , self.read , 1))
    
    #![bound::write]
    def write(self, _csobject:CSObject):
        print(_csobject.__str__())
        return CSObject.new_nulltype()
    
    #![bound::read]
    def read(self, _csobject:CSObject):
        from cshelpers import __resolve__
        """
        """
        _result = ""
        try:
            _fileobj = open(__resolve__(_csobject.__str__()), "r")
            _result  = _fileobj.read()
            _fileobj.close()
        except IOError:
            return False
        return CSObject.new_string(_result)
    

    def __str__(self):
        return f"{type(self).__name__}"

