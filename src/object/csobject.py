
from cstoken import CSToken
from errortoken import show_error
from hashmap import hasher, HashMap


# for typing
class CSObject(HashMap):pass
def CSMalloc(_csobject:CSObject):pass
def reformatError(_message:str, _token:CSToken):pass
def ThrowError(_csexceptionobject:CSObject, _error_token:CSToken):pass


class CSObject(HashMap):
    """ Represents Object in CScript
    """
    dtype = "CSObject"
    
    def __init__(self):
        super().__init__()
        # initilize
        self.dtype = type(self).__name__
    
    def get(self, _key: str):
        if  type(self) == CSObject and _key == "this":
            return self
        return super().get(_key)
    
    # ![bound::toString]
    def toString(self):
        """ toString
            
            Returns
            -------
            CSString
        """
        return CSObject.new_string(self.__str__())
    
    def isPointer(self):
        return False
    
    def __str__(self):
        """ Modify __str__() if yo want to change how it looks when its printed
            | Do not modify tostring()
            ;
        """
        _keys = self.keys()
        _attrib = ""
        for k in range(len(_keys)):

            _attrib += f"{_keys[k]}: {self.get(_keys[k]).__str__()}"

            if  k < (len(_keys) - 1):
                _attrib += ", "

        return "{" + f"{_attrib}" + "}"
    
    @staticmethod
    def new():
        _object = CSObject()
        return _object

    @staticmethod
    def new_integer(_data:int):
        import csinteger
        _int = csinteger.CSInteger(_data)
        del csinteger
        return CSMalloc(_int)

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
        return CSMalloc(_flt)

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
        return CSMalloc(_str)
    
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
        return CSMalloc(_bool)

    @staticmethod
    def new_nulltype():
        """ Creates raw null object

            Returns
            -------
            CSNullType
        """
        import csnulltype
        _null = csnulltype.CSNullType()
        del csnulltype
        return CSMalloc(_null)
    
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
        return _array

    @staticmethod
    def new_callable(_name:str, _parameters:list, _instructions:list):
        """ Creates callable

            Returns
            -------
            CSCallable
        """
        import cscallable
        _function = cscallable.CSCallable(_name, len(_parameters), _parameters, _instructions)
        del cscallable
        return _function
    
    # ======================================== DUNDER METHODS|
    # =======================================================|
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
        
    def subscript(self, _subscript_location:CSToken, _expr:CSObject):
        """ Called when [...](subscript) operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("%s is not subscriptible" % self.dtype, _subscript_location)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def call(self, _call_location:CSToken, _arg_count:int):
        """ Called when (...)(call) operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("%s is not callable" % self.dtype, _call_location)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

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
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type %s" % (_opt.token, self.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def bin_not(self, _opt:CSToken):
        """ Called when unary ! operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type %s" % (_opt.token, self.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def positive(self, _opt:CSToken):
        """ Called when unary + operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type %s" % (_opt.token, self.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def negative(self, _opt:CSToken):
        """ Called when unary - operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type %s" % (_opt.token, self.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def pow(self, _opt:CSToken, _object:CSObject):
        """ Called when power operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def mul(self, _opt:CSToken, _object:CSObject):
        """ Called when mul operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def div(self, _opt:CSToken, _object:CSObject):
        """ Called when div operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def mod(self, _opt:CSToken, _object:CSObject):
        """ Called when mod operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def add(self, _opt:CSToken, _object:CSObject):
        """ Called when add operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def sub(self, _opt:CSToken, _object:CSObject):
        """ Called when sub operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def lshift(self, _opt:CSToken, _object:CSObject):
        """ Called when left shift operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def rshift(self, _opt:CSToken, _object:CSObject):
        """ Called when right shift operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def lt(self, _opt:CSToken, _object:CSObject):
        """ Called when lessthan operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def lte(self, _opt:CSToken, _object:CSObject):
        """ Called when lessthan equal operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def gt(self, _opt:CSToken, _object:CSObject):
        """ Called when greaterthan operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def gte(self, _opt:CSToken, _object:CSObject):
        """ Called when greaterthan equal operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
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
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def neq(self, _opt:CSToken, _object:CSObject):
        """ Called when not equal

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def bit_and(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise and operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def bit_xor(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise xor operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def bit_or(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise or operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    # for compile time constant evaluation
    def log_and(self, _opt:CSToken, _object:CSObject):
        """ Called when logic and operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    # for compile time constant evaluation
    def log_or(self, _opt:CSToken, _object:CSObject):
        """ Called when logic or operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = reformatError("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error


# malloc
def CSMalloc(_csobject:CSObject):
    # import
    from cscriptvm.csvm import CSVM as VM

    _object = VM.VHEAP.allocate(_csobject)
    del VM

    # return object
    return _object


def reformatError(_message:str, _token:CSToken):
    """ By default, the entire error is string, not an exception.

        Prameters
        ---------
        _csexceptionobject : CSObject
        _token             : CSToken
    """
    _error = CSObject.new_string(
        ("[%s:%d:%d] CSTypeError: %s" % (_token.fsrce, _token.yS, _token.xS, _message))
        + "\n" 
        + _token.trace
    )
    return _error


def ThrowError(_csexceptionobject:CSObject):
    from cscriptvm.csvm import CSVM as VM
    VM.throw_error(_csexceptionobject)
    # delete vm locally
    del VM
