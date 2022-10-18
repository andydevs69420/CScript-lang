

from cstoken import CSToken
from errortoken import show_error
from hashmap import hasher, HashMap

from cscriptvm.csmemory2 import CSMemory

class CSObject(HashMap):pass
class CSObject(HashMap):
    """ Represents Object in CScript
    """
    dtype = "CSObject"
    
    def __init__(self):
        super().__init__()
        # initilize
        self.dtype  = type(self).__name__
        self.static = []
 
    # ![bound::toString]
    def toString(self):
        """ toString
            
            Returns
            -------
            CSString
        """
        _keys = self.keys()
        _attrib = ""
        for k in range(len(_keys)):
            _attrib += f"{_keys[k]}: {self.get(_keys[k]).__str__()}"
        
            if  k < (len(_keys) - 1):
                _attrib += ", "

        return CSObject.new_string("{" + f"{_attrib}" + "}")
    
    def get(self, _key: str):
        if  type(self) == CSObject and _key == "this":
            return self
        return super().get(_key)
    
    def __str__(self):
        return self.toString().__str__()
    
    @staticmethod
    def new():
        _object = CSObject()
        return CSMemory.CSMalloc(_object)

    @staticmethod
    def new_integer(_data:int):
        import csinteger
        _int = csinteger.CSInteger(_data)
        del csinteger
        return CSMemory.CSMalloc(_int)

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
        return CSMemory.CSMalloc(_flt)

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
        return CSMemory.CSMalloc(_str)
    
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
        return CSMemory.CSMalloc(_bool)

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
        return CSMemory.CSMalloc(_null)
    
    @staticmethod
    def new_array():
        """ Creates array object

            Returns
            -------
            CSArray
        """
        import csarray
        _array = csarray.CSArray()
        del csarray
        return CSMemory.CSMalloc(_array)

    @staticmethod
    def new_callable(_name:str, _parameters:list, _instructions:list):
        """ Creates callable

            Returns
            -------
            CSCallable
        """
        import cscallable
        _function = cscallable.CSCallable(_name,_parameters, _instructions)
        del cscallable
        return CSMemory.CSMalloc(_function)
    
    # ================= DUNDER METHODS|
    # ================================|
    # must be private!. do not include as attribute
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

    def getAttribute(self, _attr:CSToken):
        """ Called when "object->property"

            Parameters
            ----------
            _attr : CSToken
        """
        # throws error
        if  not self.hasAttribute(_attr.token):
            raise AttributeError(f"{type(self).__name__} has no attribute '{_attr.token}'")
        
        return self.get(_attr.token)
    
    def setAttribute(self, _attr:CSToken, _value:CSObject):
        """ Called when "csobject->property = csobject"

            Parameters
            ----------
            _attr  : CSToken
            _value : CSObject
        """
        # throws error
        if  not self.hasAttribute(_attr.token):
            raise AttributeError(f"{type(self).__name__} has no attribute '{_attr.token}'")
        
        self.put(_attr.token, _value)
        return _value
        
    def subscript(self, _opt:CSToken, _expr:CSObject):
        """ Called when [...](subscript) operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::subscript method must be overritten!" % self.dtype)
    
    def call(self, _opt:CSToken, _arg_count:int):
        """ Called when (...)(call) operation

            Returns
            -------
            CSObject
        """
        print(_opt.fsrce)
        show_error("%s is not callable" % self.dtype, _opt)
        raise NotImplementedError("%s::call method must be overritten!" % self.dtype)

    # ================= MAGIC METHODS|
    # ===============================|
    # must be private!. do not include as attribte
    def assertType(self, _opt:CSToken, _lhs:CSObject, _rhs:CSObject):
        """ Type assertion for CScript operation

            Prameters
            ---------
            _opt : CSToken
            _lhs : CSObject
            _rhs : CSObject

            Returns
            -------
            Any
        """

    def bit_not(self, _opt:CSToken):
        """ Called when unary ~ operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_not method must be overritten!" % self.dtype)

    def bin_not(self, _opt:CSToken):
        """ Called when unary ! operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bin_not method must be overritten!" % self.dtype)
    
    def positive(self, _opt:CSToken):
        """ Called when unary + operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::positive method must be overritten!" % self.dtype)
    
    def negative(self, _opt:CSToken):
        """ Called when unary - operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::negaive method must be overritten!" % self.dtype)

    def pow(self, _opt:CSToken, _object:CSObject):
        """ Called when power operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::pow method must be overritten!" % self.dtype)

    def mul(self, _opt:CSToken, _object:CSObject):
        """ Called when mul operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::mul method must be overritten!" % self.dtype)
    
    def div(self, _opt:CSToken, _object:CSObject):
        """ Called when div operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::div method must be overritten!" % self.dtype)
    
    def mod(self, _opt:CSToken, _object:CSObject):
        """ Called when mod operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::mod method must be overritten!" % self.dtype)

    def add(self, _opt:CSToken, _object:CSObject):
        """ Called when add operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::add method must be overritten!" % self.dtype)
    
    def sub(self, _opt:CSToken, _object:CSObject):
        """ Called when sub operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::sub method must be overritten!" % self.dtype)
    
    def lshift(self, _opt:CSToken, _object:CSObject):
        """ Called when left shift operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::lshift method must be overritten!" % self.dtype)
    
    def rshift(self, _opt:CSToken, _object:CSObject):
        """ Called when right shift operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::rshift method must be overritten!" % self.dtype)
    
    def lt(self, _opt:CSToken, _object:CSObject):
        """ Called when lessthan operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::lt method must be overritten!" % self.dtype)

    def lte(self, _opt:CSToken, _object:CSObject):
        """ Called when lessthan equal operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::lte method must be overritten!" % self.dtype)
    
    def gt(self, _opt:CSToken, _object:CSObject):
        """ Called when greaterthan operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::gt method must be overritten!" % self.dtype)

    def gte(self, _opt:CSToken, _object:CSObject):
        """ Called when greaterthan equal operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::gte method must be overritten!" % self.dtype)
    
    def equals(self, _object:CSObject):
        """ Raw equals

            Returns
            -------
            bool
        """
        return self.get("this") == _object.get("this")

    def eq(self, _opt:CSToken, _object:CSObject):
        """ Called when equal

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::eq method must be overritten!" % self.dtype)
    
    def neq(self, _opt:CSToken, _object:CSObject):
        """ Called when not equal

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::neq method must be overritten!" % self.dtype)

    def bit_and(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise and operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_and method must be overritten!" % self.dtype)
    
    def bit_xor(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise xor operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_xor method must be overritten!" % self.dtype)
    
    def bit_or(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise or operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::bit_or method must be overritten!" % self.dtype)
    
    # for compile time constant evaluation
    def log_and(self, _opt:CSToken, _object:CSObject):
        """ Called when logic and operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::log_and method must be overritten!" % self.dtype)
    
    # for compile time constant evaluation
    def log_or(self, _opt:CSToken, _object:CSObject):
        """ Called when logic or operation

            Returns
            -------
            CSObject
        """
        raise NotImplementedError("%s::log_or method must be overritten!" % self.dtype)