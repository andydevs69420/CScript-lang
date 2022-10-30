
from obj_utils.csclassnames import CSClassNames
from cstoken import CSToken
from base.hashmap import hasher, HashMap


# for typing
class CSObject(HashMap):pass


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

class CSObject(object):
    """ Represents Object in CScript
    """

    TYPE_STRING= "typeString"
    TO_STRING  = "toString"

    
    def __init__(self):
        # ======== memory flags|
        # =====================|
        self.offset = -69420
        self.marked = False

        self.dtype = CSClassNames.CSObject
        self.thiso = HashMap()
        self.proto = HashMap()
    
    def initializeBound(self):
        self.proto.put(CSObject.TYPE_STRING, CSObject.new_bound_method(CSObject.TYPE_STRING, self.typeString, 0))
        self.proto.put(CSObject.TO_STRING  , CSObject.new_bound_method(CSObject.TO_STRING  , self.toString  , 0))
    
    # ======================== BOUNDS|
    # ===============================|

    #![bound::runtimeType]
    def typeString(self):
        """ typeString
            
            Returns
            -------
            CSString
        """
        return CSObject.new_string(self.dtype)

    #![bound::toString]
    def toString(self):
        """ toString
            
            Returns
            -------
            CSString
        """
        return CSObject.new_string(self.__str__())
    
    # ======================== PYTHON|
    # ===============================|
    def all(self):
        return [self.thiso.get(_k) for _k in self.thiso.keys()]
    
    def python(self):
        """ Converts CSObject to Python Object
        """
        raise NotImplementedError("%s::python must be ovritten!" % self.dtype)

    def __str__(self):
        """ Modify __str__() if yo want to change how it looks when its printed
            | Do not modify tostring()
            ;
        """
        _keys   = self.thiso.keys()
        _attrib = ""
        for k in range(len(_keys)):
            _attrib += f"{_keys[k]}: {self.thiso.get(_keys[k]).__str__()}"

            if  k < (len(_keys) - 1):
                _attrib += ", "

        return "{" + f"{_attrib}" + "}"
    
    @staticmethod
    def new_object():
        _object = CSObject()
        return _object

    @staticmethod
    def new_module():
        from user_defined.csmodule import CSModule
        _module = CSModule()
        del CSModule
        return CSMalloc(_module)

    @staticmethod
    def new_integer(_data:int):
        from primitive.csinteger import CSInteger
        _int = CSInteger(_data)
        del CSInteger
        return _int

    @staticmethod
    def new_double(_data:float):
        """ Creates raw double object

            Returns
            -------
            CSDouble
        """
        from primitive.csdouble import CSDouble
        _flt = CSDouble(_data)
        del CSDouble
        return _flt

    @staticmethod
    def new_string(_data:str):
        """ Creates raw string object

            Returns
            -------
            CSString
        """
        from non_primitive.csstring import CSString
        _str = CSString(_data)
        del CSString
        return _str
    
    @staticmethod
    def new_boolean(_data:str):
        """ Creates raw boolean object

            Returns
            -------
            CSBoolean
        """
        from primitive.csboolean import CSBoolean
        _bool = CSBoolean(_data)
        del CSBoolean
        return _bool

    @staticmethod
    def new_nulltype():
        """ Creates raw null object

            Returns
            -------
            CSNullType
        """
        import primitive.csnulltype as csnulltype
        _null = csnulltype.CSNullType()
        del csnulltype
        return _null
    
    @staticmethod
    def new_array():
        """ Creates array object

            Returns
            -------
            CSArray
        """
        import non_primitive.csarray as csarray
        _array = csarray.CSArray()
        del csarray
        return _array
    
    @staticmethod
    def new_array_from_PyList(_pyList:list):
        _array = CSObject.new_array()
        for v in _pyList:
            _value = ...
            if  type(v) == int:
                _value = CSObject.new_integer(v)
            elif  type(v) == float:
                _value = CSObject.new_double(v)
            elif type(v) == str:
                _value = CSObject.new_string(v)
            elif type(v) == bool:
                _value = CSObject.new_boolean("true" if v else "false")
            elif type(v) == dict:
                # watch! recursion error
                _value = CSObject.new_map_fromDict(v)
            elif type(v) == list:
                # watch! recursion error
                _value = CSObject.new_array_fromPyList(v)
            else:
                raise TypeError("unsupported type %s" % type(v).__name__)
            
            _array.push(_value)

        return _array
    
    @staticmethod
    def new_map():
        """ Creates map object

            Returns
            -------
            CSMap
        """
        import non_primitive.csmap as csmap
        _map = csmap.CSMap()
        del csmap
        return _map
    
    @staticmethod
    def new_map_fromPyDict(_pyDict:dict):
        _map = CSObject.new_map()

        for k, v in zip(_pyDict.keys(), _pyDict.values()):
            _value = ...
            if  type(v) == int:
                _value = CSObject.new_integer(v)
            elif  type(v) == float:
                _value = CSObject.new_double(v)
            elif type(v) == str:
                _value = CSObject.new_string(v)
            elif type(v) == bool:
                _value = CSObject.new_boolean("true" if v else "false")
            elif type(v) == dict:
                # watch! recursion error
                _value = CSObject.new_map_fromDict(v)
            elif type(v) == list:
                # watch! recursion error
                _value = CSObject.new_array_fromPyList(v)
            else:
                raise TypeError("unsupported type %s" % type(v).__name__)

            _map.put(k.__str__(), _value)

        return _map

    @staticmethod
    def new_callable(_name:str, _parameters:list, _instructions:list):
        """ Creates callable

            Returns
            -------
            CSCallable
        """
        from user_defined.cscallable import CSCallable
        _function = CSCallable(_name, len(_parameters), _parameters, _instructions)
        del CSCallable
        return _function
    
    @staticmethod
    def new_class(_name:str):
        """ Creates class template

            Returns
            -------
            CSClass
        """
        from user_defined.csclass import CSClass
        _class = CSClass(_name)
        del CSClass
        return _class
    
    @staticmethod
    def new_bound_method(_name:str, _pyCallable:callable, _parameter_count:int):
        from user_defined.csbound import CSBound
        _bound = CSBound(_name, _pyCallable, _parameter_count)
        del CSBound
        return _bound
    
    @staticmethod
    def new_class_instance(_name:str):
        """ Creates class instance from class template

            Returns
            -------
            CSClass
        """
        from user_defined.csclassinstance import CSClassInstance
        _class = CSClassInstance(_name)
        del CSClassInstance
        return CSMalloc(_class)
    
    @staticmethod
    def new_class_bound_method(_thisref:CSObject, _pyCallable:callable):
        from user_defined.csclassboundmethod import CSClassBoundMethod
        _bound = CSClassBoundMethod(_thisref, _pyCallable)
        del CSClassBoundMethod
        return _bound
    
    @staticmethod
    def new_raw_function(_name:str, _param_count:int, _pyCallable:callable):
        from system.csbuiltinfunction import CSBuiltinFunction
        _bound = CSBuiltinFunction(_name, _param_count, _pyCallable)
        del CSClassBoundMethod
        return _bound

    @staticmethod
    def new_exception(_message:str, _location:CSToken):
        """ Creates exception

            Returns
            -------
            CSException
        """
        import default_error.csexception as csexception
        _exception = csexception.CSException(_message, _location)
        del csexception
        return _exception
    
    @staticmethod
    def new_type_error(_message:str, _location:CSToken):
        """ Creates typerror|exception

            Returns
            -------
            CSTypeError
        """
        import default_error.csexception as csexception
        _exception = csexception.CSTypeError(_message, _location)
        del csexception
        return _exception
    
    @staticmethod
    def new_attrib_error(_message:str, _location:CSToken):
        """ Creates attribute error|exception

            Returns
            -------
            CSAttributeError
        """
        import default_error.csexception as csexception
        _exception = csexception.CSAttributeError(_message, _location)
        del csexception
        return _exception
    
    @staticmethod
    def new_index_error(_message:str, _location:CSToken):
        """ Creates index error|exception

            Returns
            -------
            CSIndexError
        """
        import default_error.csexception as csexception
        _exception = csexception.CSIndexError(_message, _location)
        del csexception
        return _exception
        
    
    # ========================= EVENT|
    # ===============================|
    # must be private!. do not include as attribute

    def getAttribute(self, _attr:CSToken):
        """ Called when "object->property"

            Parameters
            ----------
            _attr : CSToken
        """
        # throws error
        if  not (self.thiso.hasKey(_attr.token) or self.proto.hasKey(_attr.token)):
            # = format string|
            _error = CSObject.new_attrib_error(f"{type(self).__name__}({self.__str__()}) has no attribute '{_attr.token}'", _attr)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        if  self.thiso.hasKey(_attr.token):\
        return self.thiso.get(_attr.token)
        
        return self.proto.get(_attr.token)
    
    def setAttribute(self, _attr:CSToken, _value:CSObject):
        """ Called when "csobject->property = csobject"

            Parameters
            ----------
            _attr  : CSToken
            _value : CSObject
        """
        # throws error
        if  not (self.thiso.hasKey(_attr.token) or self.proto.hasKey(_attr.token)):
            # = format string|
            _error = CSObject.new_attrib_error(f"{type(self).__name__}({self.__str__()}) has no attribute '{_attr.token}'", _attr)

            # === throw error|
            # ===============|
            ThrowError(_error)

            # == return error|
            # ===============|
            return _error
        
        if  self.thiso.hasKey(_attr.token):
            self.thiso.put(_attr.token, _value)
            return _value
        
        self.proto.put(_attr.token, _value)
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
    
    def new_op(self, _opt:CSToken):
        """ Called when unary new operation

            Returns
            -------
            CSObject
        """
        # = format string|
        _error = CSObject.new_type_error("right-hand expression \"%s(%s)\" is not a class" % (self.dtype, self.__str__()), _opt)

        # === throw error|
        # ===============|
        ThrowError(_error)

        # == return error|
        # ===============|
        return _error

    def bit_not(self, _opt:CSToken):
        """ Called when unary ~ operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)

    def bin_not(self, _opt:CSToken):
        """ Called when unary ! operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)
    
    def positive(self, _opt:CSToken):
        """ Called when unary + operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)
    
    def negative(self, _opt:CSToken):
        """ Called when unary - operation

            Returns
            -------
            CSObject
        """
        return self.__unary_expr_error(_opt)
    
    def __binary_expr_error(self, _opt:CSToken, _object:CSObject):
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

    def pow(self, _opt:CSToken, _object:CSObject):
        """ Called when power operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def mul(self, _opt:CSToken, _object:CSObject):
        """ Called when mul operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def div(self, _opt:CSToken, _object:CSObject):
        """ Called when div operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def mod(self, _opt:CSToken, _object:CSObject):
        """ Called when mod operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def add(self, _opt:CSToken, _object:CSObject):
        """ Called when add operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def sub(self, _opt:CSToken, _object:CSObject):
        """ Called when sub operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def lshift(self, _opt:CSToken, _object:CSObject):
        """ Called when left shift operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def rshift(self, _opt:CSToken, _object:CSObject):
        """ Called when right shift operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def lt(self, _opt:CSToken, _object:CSObject):
        """ Called when lessthan operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def lte(self, _opt:CSToken, _object:CSObject):
        """ Called when lessthan equal operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def gt(self, _opt:CSToken, _object:CSObject):
        """ Called when greaterthan operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def gte(self, _opt:CSToken, _object:CSObject):
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
        return self.python() == _object.python()

    def eq(self, _opt:CSToken, _object:CSObject):
        """ Called when equal

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def neq(self, _opt:CSToken, _object:CSObject):
        """ Called when not equal

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)

    def bit_and(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise and operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def bit_xor(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise xor operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    def bit_or(self, _opt:CSToken, _object:CSObject):
        """ Called when bitwise or operation

            Returns
            -------
            CSObject
        """
        return self.__binary_expr_error(_opt, _object)
    
    # short circuiting|default
    def log_and(self, _opt: CSToken, _object: CSObject):
        # self.assertType(_opt, self, _object)
        return self.python() and _object.python()
    
    def log_or(self, _opt: CSToken, _object: CSObject):
        # self.assertType(_opt, self, _object)
        return self.python() or _object.python()

