
from cstoken import CSToken
from hashmap import hasher, HashMap


# for typing
class CSObject(HashMap):pass
def CSMalloc(_csobject:CSObject):pass
def ThrowError(_csexceptionobject:CSObject, _error_token:CSToken):pass


class CSObject(HashMap):
    """ Represents Object in CScript
    """
    
    def __init__(self):
        super().__init__()
        # initilize
        self.dtype    = type(self).__name__
        self.offset   = -69420
        self.ismarked = False
    
    # ![bound::toString]
    def toString(self):
        """ toString
            
            Returns
            -------
            CSString
        """
        return CSObject.new_string(self.__str__())
    
    # ================ PYTHON|
    # =======================|
    def get(self, _key: str):
        if type(self) == CSObject and _key == "this": return self
        return super().get(_key)

    def all(self):
        return [self.get(_k) for _k in self.keys()]
    
    def isPointer(self):
        return False

    def __str__(self):
        """ Modify __str__() if yo want to change how it looks when its printed
            | Do not modify tostring()
            ;
        """
        _keys   = self.keys()
        _attrib = ""
        for k in range(len(_keys)):

            _attrib += f"{_keys[k]}: {self.get(_keys[k]).__str__()}"

            if  k < (len(_keys) - 1):
                _attrib += ", "

        return "{" + f"{_attrib}" + "}"
    
    @staticmethod
    def new(_allocate:bool=True):
        _object = CSObject()
        return CSMalloc(_object) if _allocate else _object

    @staticmethod
    def new_integer(_data:int, _allocate:bool=True):
        import csinteger
        _int = csinteger.CSInteger(_data)
        del csinteger
        return CSMalloc(_int) if _allocate else _int

    @staticmethod
    def new_double(_data:float, _allocate:bool=True):
        """ Creates raw double object

            Returns
            -------
            CSDouble
        """
        import csdouble
        _flt = csdouble.CSDouble(_data)
        del csdouble
        return CSMalloc(_flt) if _allocate else _flt

    @staticmethod
    def new_string(_data:str, _allocate:bool=True):
        """ Creates raw string object

            Returns
            -------
            CSString
        """
        import csstring
        _str = csstring.CSString(_data)
        del csstring
        return CSMalloc(_str) if _allocate else _str
    
    @staticmethod
    def new_boolean(_data:str, _allocate:bool=True):
        """ Creates raw boolean object

            Returns
            -------
            CSBoolean
        """
        import csboolean
        _bool = csboolean.CSBoolean(_data)
        del csboolean
        return CSMalloc(_bool) if _allocate else _bool

    @staticmethod
    def new_nulltype(_allocate:bool=True):
        """ Creates raw null object

            Returns
            -------
            CSNullType
        """
        import csnulltype
        _null = csnulltype.CSNullType()
        del csnulltype
        return CSMalloc(_null) if _allocate else _null
    
    @staticmethod
    def new_array(_allocate:bool=True):
        """ Creates array object

            Returns
            -------
            CSArray
        """
        import csarray
        _array = csarray.CSArray()
        del csarray
        return CSMalloc(_array) if _allocate else _array
    
    @staticmethod
    def new_array_from_PyList(_pyList:list, _allocate:bool=True):
        _array = CSObject.new_array(_allocate)
        for v in _pyList:
            _value = ...
            if  type(v) == int:
                _value = CSObject.new_integer(v, _allocate)
            elif  type(v) == float:
                _value = CSObject.new_double(v, _allocate)
            elif type(v) == str:
                _value = CSObject.new_string(v, _allocate)
            elif type(v) == bool:
                _value = CSObject.new_boolean("true" if v else "false", _allocate)
            elif type(v) == dict:
                # watch! recursion error
                _value = CSObject.new_map_fromDict(v, _allocate)
            elif type(v) == list:
                # watch! recursion error
                _value = CSObject.new_array_fromPyList(v, _allocate)
            else:
                raise TypeError("unsupported type %s" % type(v).__name__)
            
            _array.push(_value)

        return _array
    
    @staticmethod
    def new_map(_allocate:bool=True):
        """ Creates map object

            Returns
            -------
            CSMap
        """
        import csmap
        _map = csmap.CSMap()
        del csmap
        return CSMalloc(_map) if _allocate else _map
    
    @staticmethod
    def new_map_fromPyDict(_pyDict:dict, _allocate:bool=True):
        _map = CSObject.new_map(_allocate)

        for k, v in zip(_pyDict.keys(), _pyDict.values()):
            _value = ...
            if  type(v) == int:
                _value = CSObject.new_integer(v, _allocate)
            elif  type(v) == float:
                _value = CSObject.new_double(v, _allocate)
            elif type(v) == str:
                _value = CSObject.new_string(v, _allocate)
            elif type(v) == bool:
                _value = CSObject.new_boolean("true" if v else "false", _allocate)
            elif type(v) == dict:
                # watch! recursion error
                _value = CSObject.new_map_fromDict(v, _allocate)
            elif type(v) == list:
                # watch! recursion error
                _value = CSObject.new_array_fromPyList(v, _allocate)
            else:
                raise TypeError("unsupported type %s" % type(v).__name__)

            _map.put(k.__str__(), _value)

        return _map

    @staticmethod
    def new_callable(_name:str, _parameters:list, _instructions:list, _allocate:bool=True):
        """ Creates callable

            Returns
            -------
            CSCallable
        """
        import cscallable
        _function = cscallable.CSCallable(_name, len(_parameters), _parameters, _instructions)
        del cscallable
        return CSMalloc(_function) if _allocate else _function
    
    @staticmethod
    def new_exception(_message:str, _location:CSToken, _allocate:bool=True):
        """ Creates exception

            Returns
            -------
            CSException
        """
        import csexception
        _exception = csexception.CSException(_message, _location)
        del csexception
        return CSMalloc(_exception) if _allocate else _exception
    
    @staticmethod
    def new_type_error(_message:str, _location:CSToken, _allocate:bool=True):
        """ Creates typerror|exception

            Returns
            -------
            CSTypeError
        """
        import csexception
        _exception = csexception.CSTypeError(_message, _location)
        del csexception
        return CSMalloc(_exception) if _allocate else _exception
    
    @staticmethod
    def new_attrib_error(_message:str, _location:CSToken, _allocate:bool=True):
        """ Creates attribute error|exception

            Returns
            -------
            CSAttributeError
        """
        import csexception
        _exception = csexception.CSAttributeError(_message, _location)
        del csexception
        return CSMalloc(_exception) if _allocate else _exception
    
    @staticmethod
    def new_index_error(_message:str, _location:CSToken, _allocate:bool=True):
        """ Creates index error|exception

            Returns
            -------
            CSIndexError
        """
        import csexception
        _exception = csexception.CSIndexError(_message, _location)
        del csexception
        return CSMalloc(_exception) if _allocate else _exception
        
    
    # ========================= EVENT|
    # ===============================|
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
            # = format string|
            _error = CSObject.new_attrib_error(f"{type(self).__name__}({self.__str__()}) has no attribute '{_attr.token}'", _attr)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
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
            # = format string|
            _error = CSObject.new_attrib_error(f"{type(self).__name__}({self.__str__()}) has no attribute '{_attr.token}'", _attr)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        self.put(_attr.token, _value)
        return _value
        
    def subscript(self, _subscript_location:CSToken, _expr:CSObject):
        """ Called when [...](subscript) operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = CSObject.new_type_error("%s is not subscriptible" % self.dtype, _subscript_location)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error
    
    def subscriptSet(self, _subscript_location:CSToken, _attribute:CSObject, _new_value:CSObject):
        """ Called when subscript is assigned x[100] = 2
        """
        # = format string|
        _error = CSObject.new_attrib_error(f"{type(self).__name__}({self.__str__()}) has no attribute '%s'" % _attribute.__str__(), _subscript_location)

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
        _error = CSObject.new_type_error(f"%s({self.__str__()}) is not callable" % self.dtype, _call_location)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    # ==================== OPERATIONS|
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

    def __unary_expr_error(self, _opt:CSToken):
        # = format string|
        _error = CSObject.new_type_error("unsupported operator \"%s\" for type %s" % (_opt.token, self.dtype), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def bit_not(self, _opt:CSToken, _allocate:bool=True):
        """ Called when unary ~ operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)

    def bin_not(self, _opt:CSToken, _allocate:bool=True):
        """ Called when unary ! operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)
    
    def positive(self, _opt:CSToken, _allocate:bool=True):
        """ Called when unary + operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)
    
    def negative(self, _opt:CSToken, _allocate:bool=True):
        """ Called when unary - operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)
    
    def __binary_expr_error(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called if not implemented operation
        """
        # = format string|
        _error = CSObject.new_type_error("unsupported operator \"%s\" for type(s) %s and %s" % (_opt.token, self.dtype, _object.dtype), _opt)
    
        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def pow(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when power operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def mul(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when mul operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def div(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when div operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def mod(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when mod operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def add(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when add operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def sub(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when sub operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def lshift(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when left shift operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def rshift(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when right shift operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def lt(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when lessthan operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def lte(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when lessthan equal operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def gt(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when greaterthan operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def gte(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when greaterthan equal operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def equals(self, _object:CSObject):
        """ Raw equals

            Returns
            -------
            bool
        """
        return self.get("this") == _object.get("this")

    def eq(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when equal

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def neq(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when not equal

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def bit_and(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when bitwise and operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def bit_xor(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when bitwise xor operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def bit_or(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when bitwise or operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    # for compile time constant evaluation
    def log_and(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when logic and operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    # for compile time constant evaluation
    def log_or(self, _opt:CSToken, _object:CSObject, _allocate:bool=True):
        """ Called when logic or operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)


# malloc
def CSMalloc(_csobject:CSObject):
    # import
    from cscriptvm.csvm import CSVM as VM

    _object = VM.VHEAP.allocate(_csobject)
    del VM

    # return object
    return _object


def ThrowError(_csexceptionobject:CSObject):
    from cscriptvm.csvm import CSVM as VM
    VM.throw_error(_csexceptionobject)
    # delete vm locally
    del VM



def nonRecursiveToSting(_csobject:CSObject):
    _keys   = _csobject.keys()
    _attrib = ""
    for k in range(len(_keys)):
        _ckey = _csobject.get(_keys[k]).__str__() if _keys[k] != "this" else _csobject.get("this")
        _attrib += f"{_keys[k]}: {_ckey}"

        if  k < (len(_keys) - 1):
            _attrib += ", "

    return "{" + f"{_attrib}" + "}"

