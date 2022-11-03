from compiler import Instruction
from compiler import CSOpCode

# builtins
from csbuiltins import CSObject
from csbuiltins import csrawcode
from csbuiltins import CSString
from csbuiltins import CSInteger
from csbuiltins import CSDouble
from csbuiltins.csbuiltins import csB__double_proto, csB__integer_proto, csB__object_proto
from csbuiltins.csfunction import CSFunction
from csbuiltins.csnulltype import CSNullType
from csbuiltins.cstypes import CSTypes

# utility
from utility import __throw__

class CSXEnvironment(object):
    """ environment while running
    """
    def __init__(self):
        self.scope = [Scope()] # scope 0 is the global scope
        self.stack = STACK()
        self.vheap = CSXMemory(self)
        self.current = None


class STACK(object):
    def __init__(self):
        self.__internal = []
    
    def push(self, _any:CSObject):
        self.__internal.append(_any)

    def poll(self):
        if  len(self.__internal) > 0:
            return self.__internal.pop()
        return None
    
    def peek(self):
        return self.__internal[-1]


class CSXMemory(object):
    """ Serves as heap memory
    """

    def __init__(self, _env:CSXEnvironment):
        self.__bucket = []
        # unused index
        self.__unused = []
        self.__scopes = _env.scope
    
    def cs__malloc(self, _csobject:CSObject):
        
        # for singleton objects!!
        assert _csobject.offset == -69420, "already in memory!"

        if  len(self.__unused) > 0:
            _csobject.offset = self.__unused[-1]
            self.__bucket[self.__unused[-1]] = _csobject
            return self.__bucket[self.__unused.pop()]
        
        # creates new slot
        _csobject.offset = len(self.__bucket)
        self.__bucket.append(_csobject)
        return self.__bucket[-1]
    
    def cs__object_at(self, _address_offset_index:int):
        return self.__bucket[_address_offset_index]

    def gmark__phase(self):
        ...
    
    def sweep__phase(self):
        ...

    def collect(self):
        self.gmark__phase()
        self.sweep__phase()


class Scope(object):
    """ Acts as symbol table

        Parameters
        ----------
        _parent(optional) : Scope|None
    """

    def __init__(self, _parent=None):
        self.parent  = _parent
        self.symbols = ({
            # var_name: int->offset of object
        })
    
    def insert(self, _symbol:str, **_props):
        self.symbols[_symbol] = _props
    
    def update(self, _symbol:str, **_props):
        assert self.exists(_symbol, False), "null possibility not handled!"
        self.symbols[_symbol].update(_props)
    
    def lookup(self, _symbol:str):
        assert self.exists(_symbol, False), "null possibility not handled!"
        if  (_symbol in self.symbols.keys()):
            return self.symbols[_symbol]
        
        # until parent is none
        _parent = self.parent
        while _parent:
            if  _parent.exists(_symbol, _local=True):
                return _parent.lookup(_symbol)
            _parent = _parent.parent
        
        raise Exception("unhandled!!!")
    
    def exists(self, _symbol:str, _local:bool=True):
        if  (_symbol in self.symbols.keys()):
            return True
        
        if _local: return False

        # search while parent is None
        _node = self.parent
        while _node:
            if  _node.exists(_symbol):
                return True
            _node = _node.parent
        
        return False


""" Begin runtime functions
"""


def cs__error(_env:CSXEnvironment, _message:str):
    return __throw__(_message)

def cs__get_constructor(
    _env:CSXEnvironment, 
    _constructor_name:str
):
    _info = _env.scope[-1].lookup(_constructor_name)
    _type = \
        _env.vheap\
        .cs__object_at(_info["_address"])
    return _type


def cs__get_proto(
    _env:CSXEnvironment, 
    _constructor_name:str,
    _prototype_name:str
):
    _type  = cs__get_constructor(_env, _constructor_name)
    _proto = _type.get(_prototype_name)
    return _proto


def cs__define_prop(_env:CSXEnvironment, _name:str, _csObject):
    _env.scope[-1].insert(_name, _address=_csObject.offset,_global=False)

# ======================== OBJECT CREATION|
# ========================================|
def cs__new_number(_env:CSXEnvironment, _raw_py_number:int|float):
    """ Allocates new int|double
    """
    if  type(_raw_py_number) == int:
        _env.stack.push(CSInteger(_raw_py_number))
        cs__raw_call(_env, cs__get_proto(_env, CSTypes.TYPE_CSINTEGER, "constructor"), 1)
    else:
        _env.stack.push(CSDouble(_raw_py_number))
        cs__raw_call(_env, cs__get_proto(_env, CSTypes.TYPE_CSDOUBLE , "constructor"), 1)


def cs__new_string(_env:CSXEnvironment, _raw_py_string:str):
    """ Allocates new string
    """
    _env.stack.push(_env.vheap.cs__malloc(CSString(_raw_py_string)))


def cs__new_null(_env:CSXEnvironment):
    """ Allocates new string
    """
    _env.stack.push(_env.vheap.cs__malloc(CSNullType()))


def cs__new_code(_env:CSXEnvironment, _raw_code:csrawcode):
    """ Allocates new code

        Parameters
        ----------
        _env : CSXEnvironment
        _raw_code : csrawcode
    """
    _env.stack.push(_env.vheap.cs__malloc(_raw_code))


def cs__new_function(_env:CSXEnvironment):
    """ Allocates function
    """
    _fname = _env.stack.poll()
    _fargc = _env.stack.poll()
    _fcode = _env.stack.poll()
    _env.stack.push(_env.vheap.cs__malloc(CSFunction(_fname, _fargc, _fcode)))


def cs__new_class(_env:CSXEnvironment, _size:int):
    """ Allocates function
    """
    _csclass = cs__get_proto(_env, CSTypes.TYPE_CSOBJECT, "constructor")\
               .call([_env, None])
    _csclass.type = _env.stack.poll().this

    for _r in range(_size):
        _key = _env.stack.poll()
        _val = _env.stack.poll()
        _csclass.put(_key.this, _val)

    _env.stack.push(_csclass)


# ======================= OBJECT RETRIEVAL|
# ========================================|

def cs__var_exists(_env:CSXEnvironment, _var_name:str):
    """ Check if variable exists in local->parent scope

        starts at local(important)
            until parent is None
        
        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
    """
    return _env.scope[-1].exists(_var_name, _local=False)


def cs__make_variable(_env:CSXEnvironment, _var_name:str, _value_address:int):
    """ Creates a new variable if target _var_name does not exists locally!

        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
        _address : int
    """
    # check if variable exists
    if  cs__var_exists(_env, _var_name):
        return cs__error(_env, "NameError: '%s' is already defined!" % _var_name)

    _env.scope[-1].insert(_var_name, _address=_value_address, _global=True)

def cs__local_exists(_env:CSXEnvironment, _var_name:str):
    """ Check if variable exists in local->parent scope

        starts at local(important)
            until parent is None
        
        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
    """
    return _env.scope[-1].exists(_var_name, _local=True)

def cs__make_local(_env:CSXEnvironment, _var_name:str, _value_address:int):
    """ Creates a new local variable if target _var_name does not exists locally!

        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
        _address : int
    """
    # check if variable exists
    if  cs__local_exists(_env, _var_name):
        return cs__error(_env, "NameError: '%s' is already defined in scope!" % _var_name)

    _env.scope[-1].insert(_var_name, _address=_value_address, _global=False)

def cs__get_variable(_env:CSXEnvironment, _var_name:str):
    """ Retrieve variable value if exists in current scope!

        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
    """
    # check if variable exists in local->parent scope
    if  not cs__var_exists(_env, _var_name):
        return cs__error(_env, "ReferenceError: '%s' is not defined!" % _var_name)

    _ref = _env.scope[-1].lookup(_var_name)
   
    # retrieve
    _env.stack.push(_env.vheap.cs__object_at(_ref["_address"]))
    

def cs__store_name(_env:CSXEnvironment, _var_name:str, _value:CSObject):
    ...
    _env.scope[-1].update(_var_name, _address=_value.offset)

# ================================== EVENT|
# ========================================|

def cs__is_callable(_object:CSObject):
    return _object.type == CSTypes.TYPE_CSNATIVEFUNCTION or _object.type == CSTypes.TYPE_CSFUNCTION


def cs__raw_call(_env:CSXEnvironment, _csobject:CSObject, _arg_count:int):
    """
    """

    if not cs__is_callable(_csobject):\
    return cs__error(_env, "%s is not callable!" % _csobject.__str__())

    _name = _csobject.get("name")
    _argc = _csobject.get("argc")

    if _argc.this != _arg_count:\
    return cs__error(_env, "%s requires %d argument(s), got %d!" % (_name.this, _argc.this, _arg_count))

    match _csobject.type:
        case CSTypes.TYPE_CSFUNCTION:
            cs__call(_env, _csobject.get("code"))

        case CSTypes.TYPE_CSNATIVEFUNCTION:
            _args = [
                _env, # environment,
                _env.current, # this,
                # arg_0,
                # arg_1,
                # arg_N,
            ]

            for _r in range(_arg_count):_args.append(_env.stack.poll())
            # 
            _env.stack.push(_csobject.call(_args))
        case _:
            raise Exception("Error!")


def cs__call_function(_env:CSXEnvironment, _top_object:CSObject, _arg_count:int):
    """ Handles function call

        Parameters
        ----------
        _env : CSXEnvironment
        _top_object : CSObject
        _arg_count : int
    """
    # NOTE: watch recursion

    _env.scope.append(Scope(_parent=_env.scope[-1]))

    cs__raw_call(_env, _top_object, _arg_count)

    _env.scope.pop()


def cs__call_method(_env:CSXEnvironment, _top_object, _arg_count:int):
    """ Handles method call

        Parameters
        ----------
        _env : CSXEnvironment
        _top_object : CSObject
        _arg_count : int
    """
    # NOTE: watch recursion
    
    _env.scope.append(Scope(_parent=_env.scope[-1]))

    cs__define_prop(_env, "this", _env.current)

    cs__raw_call(_env, _top_object, _arg_count)

    # cleanup current
    _env.current = None

    _env.scope.pop()


def cs__get_attribute(_env:CSXEnvironment, _top_object:CSObject, _attr:str):
    """ Returns attribute of an object, otherwise error

        Parameters
        ----------
        _env : CSXEnvironment
        _top_object : CSObject
        _attr : str
    """  

    # set current object

    # check has attribute
    if not _top_object.hasKey(_attr):\
    return cs__error(_env, "AttributeError: %s has no attribute %s" % (_top_object.type, _attr))

    _env.stack.push(_top_object.get(_attr))


def cs__set_attribute(_env:CSXEnvironment, _attr:str):
    """ Sets object attribute

        Parameters
        ----------
        _env : CXEnvironment
        _attr : str
    """

    # set current object
    _top_object = _env.stack.poll()
    _top_object.put(_attr, _env.stack.poll())


def cs__get_method(_env:CSXEnvironment, _top_object:CSObject, _attr:str):
    """ Get specific method of a type

        Parameters
        ----------
        _env : CXEnvironment
        _top_object : CSObject
        _attr : str
    """

    _env.current = _top_object

    # check proto
    cs__get_variable(_env, _top_object.type)
    
    _obj = _env.stack.poll()

    if not _obj.hasKey(_attr):\
    return cs__error(_env, "AttributeError: %s has no attribute %s" % (_top_object.type, _attr))

    _env.stack.push(_obj.get(_attr))
        

def cs__construct_class(_env:CSXEnvironment, _arg_count:int):
    """
    """

    _class_proto = _env.stack.poll()

    if not _class_proto.hasKey("constructor"):\
    return cs__error(_env, "%s is not a constructor" % _class_proto.__str__())

    _constructor = _class_proto.get("constructor")

    _env.scope.append(Scope(_parent=_env.scope[-1]))

    cs__raw_call(_env, _constructor, _arg_count)

    _env.scope.pop()


def cs__call(_env:CSXEnvironment, _code:csrawcode):
    """
    """
    _ipointer = 0
    _returned = False


    for i in _code:
        print(i)

    while _ipointer < len(_code.code) and (not _returned):

        _instruction = _code.code[_ipointer]
        match _instruction.opcode:

            case CSOpCode.PUSH_INTEGER:cs__new_number(_env, _instruction.get("const"))
            case CSOpCode.PUSH_DOUBLE:cs__new_number(_env, _instruction.get("const"))
            case CSOpCode.PUSH_STRING:cs__new_string(_env, _instruction.get("const"))
            case CSOpCode.PUSH_NULL:cs__new_null(_env)
            case CSOpCode.PUSH_CODE:cs__new_code(_env, _instruction.get("code"))
            case CSOpCode.MAKE_FUNCTION:cs__new_function(_env)
            case CSOpCode.MAKE_CLASS:cs__new_class(_env, _instruction.get("size"))
            case CSOpCode.PUSH_NAME:cs__get_variable(_env, _instruction.get("name"))

            # event
            case CSOpCode.CALL:cs__call_function(_env, _env.stack.poll(), _instruction.get("size"))
            case CSOpCode.CALL_METHOD:cs__call_method(_env, _env.stack.poll(), _instruction.get("size"))
            case CSOpCode.MAKE_VAR:cs__make_variable(_env, _instruction.get("name"), _env.stack.poll().offset)
            case CSOpCode.MAKE_LOCAL:cs__make_local(_env, _instruction.get("name"), _env.stack.poll().offset)

            case CSOpCode.STORE_NAME:
                cs__store_name(_env, _instruction.get("name"), _env.stack.poll())

            # attributes
            case CSOpCode.GET_ATTRIB:
                cs__get_attribute(_env, _env.stack.poll(), _instruction.get("attr"))
            case CSOpCode.SET_ATTRIB:
                cs__set_attribute(_env, _instruction.get("attr"))
            
            case CSOpCode.GET_METHOD:
                cs__get_method(_env, _env.stack.poll(), _instruction.get("attr"))
              
            # unary
            case CSOpCode.UNARY_OP:
                match _instruction.get("opt"):
                    case "new":
                        cs__construct_class(_env, _instruction.get("size"))

            # multiplicative
            case CSOpCode.BINARY_MUL:
                _a = _env.stack.poll()
                _b = _env.stack.poll()
                cs__new_number(_env, _a.this * _b.this)
                
            case CSOpCode.BINARY_DIV:
                _a = _env.stack.poll()
                _b = _env.stack.poll()
                cs__new_number(_env, _a.this / _b.this)

            case CSOpCode.BINARY_MOD:
                _a = _env.stack.poll()
                _b = _env.stack.poll()
                cs__new_number(_env, _a.this % _b.this)

            # addetive
            case CSOpCode.BINARY_ADD:
                _a = _env.stack.poll()
                _b = _env.stack.poll()
                cs__new_number(_env, _a.this + _b.this)
            
            case CSOpCode.BINARY_SUB:
                _a = _env.stack.poll()
                _b = _env.stack.poll()
                cs__new_number(_env, _a.this - _b.this)
            
            case CSOpCode.DUP_TOP:
                _env.stack.push(_env.stack.peek())

            case CSOpCode.PRINT_OBJECT:
                _size = _instruction.get("size")
                _format = ""

                for idx in range(_size):
                    _raw_obj = _env.stack.poll()
                    _format += _raw_obj.__str__()

                    if  idx < _size - 1:
                        _format += ", "
                
                print(_format)

            case CSOpCode.POP_TOP:
                _env.stack.poll()

            case CSOpCode.RETURN_OP:
                return

            case _:
                raise NotImplementedError("invalid opcode %s" % _instruction.opcode.name)
        _ipointer += 1
    
    print("DONE!")


def cs__init_builtin(_env:CSXEnvironment):
    """
    """
    _base = csB__object_proto(_env)
    csB__double_proto(_env, _base)
    csB__integer_proto(_env, _base)
    
def cs__run(_code:csrawcode):
    _env = CSXEnvironment()

    # initialize before run
    cs__init_builtin(_env)

    # call module
    cs__call(_env, _code)




