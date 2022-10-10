

from hashmap import hasher, HashMap

class CSObject(HashMap):pass

class CSObject(HashMap):
    """ Represents Object in CScript
    """
    
    def __init__(self):
        super().__init__()
        # initilize defauls
        self.dtype = type(self).__name__
        self.proto = HashMap()
    

    # ![bound::toString]
    def toString(self):
        """ toString
            
            Returns
            -------
            CSString
        """
    
    def hasAttribute(self, _key:str):
        _bucket_index = hasher(_key) % self.bcount

        if  self.bucket[_bucket_index] == None:
            return False

        _head = self.bucket[_bucket_index]
        
        while _head:
            if  _head.nkey == _key:
                return True
            _head = _head.tail
        return False

    @staticmethod
    def new_integer(_data:int):
        import csinteger
        _int = csinteger.CSInteger(_data)
        del csinteger
        return _int

    @staticmethod
    def new_double(_data:float):
        """ Creates raw double object

            Returns
            -------
            CSDouble
        """
        import csdouble
        _flt = csdouble.CSDouble(_data)
        del csdouble
        return _flt

    @staticmethod
    def new_string(_data:str):
        """ Creates raw string object

            Returns
            -------
            CSString
        """
        import csstring
        _str = csstring.CSString(_data)
        del csstring
        return _str
    
    @staticmethod
    def new_boolean(_data:str):
        """ Creates raw boolean object

            Returns
            -------
            CSBoolean
        """
        import csboolean
        _bool = csboolean.CSBoolean(_data)
        del csboolean
        return _bool

    @staticmethod
    def new_nulltype(_data:str):
        """ Creates raw null object

            Returns
            -------
            CSNullType
        """
        import csnulltype
        _null = csnulltype.CSNullType(_data)
        del csnulltype
        return _null
        
    # ================= MAGIC METHODS
    def bit_not(self):
        """ Called when unary ~ operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_not method must be overritten!" % self.dtype)

    def bin_not(self):
        """ Called when unary ! operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bin_not method must be overritten!" % self.dtype)
    
    def positive(self):
        """ Called when unary + operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::positive method must be overritten!" % self.dtype)
    
    def negative(self):
        """ Called when unary - operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::negaive method must be overritten!" % self.dtype)

    def pow(self, _object:CSObject):
        """ Called when power operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::pow method must be overritten!" % self.dtype)

    def mul(self, _object:CSObject):
        """ Called when mul operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::mul method must be overritten!" % self.dtype)
    
    def div(self, _object:CSObject):
        """ Called when div operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::div method must be overritten!" % self.dtype)
    
    def mod(self, _object:CSObject):
        """ Called when mod operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::mod method must be overritten!" % self.dtype)

    def add(self, _object:CSObject):
        """ Called when add operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::add method must be overritten!" % self.dtype)
    
    def sub(self, _object:CSObject):
        """ Called when sub operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::sub method must be overritten!" % self.dtype)
    
    def bit_and(self, _object:CSObject):
        """ Called when bitwise and operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_and method must be overritten!" % self.dtype)
    
    def bit_xor(self, _object:CSObject):
        """ Called when bitwise xor operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_xor method must be overritten!" % self.dtype)
    
    def bit_or(self, _object:CSObject):
        """ Called when bitwise or operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_or method must be overritten!" % self.dtype)