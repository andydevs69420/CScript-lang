

from compiler import Instruction
from compiler import CSOpCode

from linkage import __ALL__ as ln

# builtins
from csbuiltins import CSTypes
from csbuiltins import CSObject
from csbuiltins import csrawcode
from csbuiltins import CSInteger
from csbuiltins import CSDouble
from csbuiltins import CSString
from csbuiltins import CSBoolean
from csbuiltins.csnativefunction import CSNativeFunction
from csbuiltins.csnulltype import CSNullType
from csbuiltins.csfunction import CSFunction

# utility
from utility import __throw__
from utility import logger

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
    
    def all(self):
        print(self.__internal)


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
        assert _csobject.offset == -69420, "double allocation!"

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


def cs__error(_env:CSXEnvironment, _message:str, _location:str):
    """
    """
    return __throw__(
        _message
        + "\n"
        + _location
    )

def cs__define_prop(_env:CSXEnvironment, _name:str, _csObject):
    """
    """
    _env.scope[-1].insert(_name, _address=_csObject.offset,_global=False)

def cs__get_prototype(
    _env:CSXEnvironment, 
    _constructor_name:str
):
    """
    """
    _info = _env.scope[-1].lookup(_constructor_name)
    _type = \
        _env.vheap\
        .cs__object_at(_info["_address"])
    return _type


def cs__get_prototype_attribute(
    _env:CSXEnvironment, 
    _constructor_name:str,
    _prototype_name:str
):
    """
    """
    _type  = cs__get_prototype(_env, _constructor_name)

    if not _type.hasKey(_prototype_name):\
    cs__error(_env, "AttributeError: %s has no attribute %s" % (_type.__str__(), _prototype_name))

    return _type.get(_prototype_name)














# ======================== OBJECT CREATION|
# ========================================|
def cs__new_number(_env:CSXEnvironment, _raw_py_number:int|float):
    """ Allocates new int|double

        Parameters
        ----------
        _env : CSXEnvironment
        _raw_py_number : int|float
    """
    if  type(_raw_py_number) == int:
        _env.stack.push(_env.vheap.cs__malloc(CSInteger(_raw_py_number)))
    else:
        _env.stack.push(_env.vheap.cs__malloc(CSDouble(_raw_py_number)))


def cs__new_string(_env:CSXEnvironment, _raw_py_string:str):
    """ Allocates new string

        Parameters
        ----------
        _env : CSXEnvironment
        _raw_py_string : str
    """
    _env.stack.push(_env.vheap.cs__malloc(CSString(_raw_py_string)))



def cs__new_boolean(_env:CSXEnvironment, _raw_py_bool:bool):
    """ Allocates|reuse boolean

        Parameters
        ----------
        _env : CSXEnvironment
        _raw_py_bool : bool
    """
    _env.stack.push(_env.vheap.cs__malloc(CSBoolean(_raw_py_bool)))



def cs__new_null(_env:CSXEnvironment):
    """ Allocates|reuse null

        Parameters
        ----------
        _env : CSXEnvironment
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

        Parameters
        ----------
        _env : CSXEnvironment
    """
    _fname = _env.stack.poll()
    _fargc = _env.stack.poll()
    _fcode = _env.stack.poll()
    _env.stack.push(_env.vheap.cs__malloc(CSFunction(_fname, _fargc, _fcode)))


def cs__new_class(_env:CSXEnvironment, _size:int):
    """ Allocates new class declairation

        Parameters
        ----------
        _env : CSXEnvironment
        _size : int
    """

    _csclass = _env.vheap.cs__malloc(CSObject())
    _csclass.type = _env.stack.poll().this

    if  cs__var_exists(_env, CSTypes.TYPE_CSOBJECT):
        # if not extended. use CSObject as super class
        _proto = cs__get_prototype(_env, CSTypes.TYPE_CSOBJECT)
        _keys = _proto.keys()
        for _k in _keys:
            _csclass.put(_k, _proto.get(_k))

    for _r in range(_size):
        _key = _env.stack.poll()
        _val = _env.stack.poll()

        # check
        if cs__has_method(_env, _csclass, _key.__str__()):\
        logger("cs__new_class", "overriding native \"%s::%s\" method..." % (_csclass.type, _key.__str__()))
        
        # put
        _csclass.put(_key.__str__(), _val)

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




def cs__make_variable(_env:CSXEnvironment, _var_name:str, _value:CSObject):
    """ Creates a new variable if target _var_name does not exists locally!

        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
        _address : int
    """
    assert not cs__var_exists(_env, _var_name), "already exists!"
    _env.scope[-1].insert(_var_name, _address=_value.offset, _global=True)




def cs__make_local(_env:CSXEnvironment, _var_name:str, _value:CSObject):
    """ Creates a new local variable if target _var_name does not exists locally!

        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
        _address : int
    """
    assert not cs__local_exists(_env, _var_name), "already exists!"
    _env.scope[-1].insert(_var_name, _address=_value.offset, _global=False)



def cs__get_variable(_env:CSXEnvironment, _var_name:str):
    """ Retrieve variable value if exists in current scope!

        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
    """
    assert cs__var_exists(_env, _var_name) or cs__local_exists(_env, _var_name), "not existed!"
    _ref = _env.scope[-1].lookup(_var_name)
   
    # retrieve
    _env.stack.push(_env.vheap.cs__object_at(_ref["_address"]))
    


def cs__store_name(_env:CSXEnvironment, _var_name:str, _value:CSObject):
    """ Re-assign variable

        Parameters
        ----------
        _env : CSXEnvironment
        _var_name : str
        _value : CSObject
    """
    assert cs__var_exists(_env, _var_name) or cs__local_exists(_env, _var_name), "var does not exist %s" % _var_name
    _env.scope[-1].update(_var_name, _address=_value.offset)











# ================================== EVENT|
# ========================================|
def cs__is_callable(_object:CSObject):
    """
    """
    return  _object.type == CSTypes.TYPE_CSNATIVEFUNCTION or \
            _object.type == CSTypes.TYPE_CSFUNCTION



def cs__raw_call(_env:CSXEnvironment, _csobject:CSFunction|CSNativeFunction, _arg_count:int):
    """ Calls a CSFunction or CSNativeFunction
    """
    assert cs__is_callable(_csobject), "not callable %s" % _csobject.__str__()

    assert _csobject.get("argc").this == _arg_count, "insufficient argument count (%d != %d) !" % (_csobject.get("argc").this, _arg_count)

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

            for _r in range(_arg_count): _args.append(_env.stack.poll())
            # 
            _env.stack.push(_csobject.call(_args))


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

    # put this to current scope
    cs__define_prop(_env, "this", _env.current)

    cs__raw_call(_env, _top_object, _arg_count)

    # cleanup current
    _env.current = None

    _env.scope.pop()


def cs__invoke_method(_env:CSXEnvironment, _csobject:CSObject, _method_name:str, _arg_count:int):
    """
    """
    assert cs__has_method(_env, _csobject, _method_name), "no method %s" % _method_name

    _env.scope.append(Scope(_parent=_env.scope[-1]))

    _env.current = _csobject

    # define this
    cs__define_prop(_env, "this", _env.current)

    cs__raw_call(_env, cs__get_prototype_attribute(_env, _csobject.type, _method_name), _arg_count)

    # cleanup current
    _env.current = None

    _env.scope.pop()



# ================================= MEMBER|
# ========================================|
def cs__has_attribute(_env:CSXEnvironment, _top_object:CSObject, _attribute:str):
    """ Checks if object has attribute

        Parameters
        ----------
        _env : CSXEnvironment
        _top_object : CSObject
        _attribute : str
    """
    if _top_object.hasKey(_attribute): return True

    # check prototype
    if  not cs__var_exists(_env, _top_object.type):
        return False
    
    _proto = cs__get_prototype(_env, _top_object.type)
    if  _proto.hasKey(_attribute):
        return True

    return False

def cs__has_method(_env:CSXEnvironment, _top_object:CSObject, _attribute:str):
    """ Checks if object has method

        Parameters
        ----------
        _env : CSXEnvironment
        _top_object : CSObject
        _attribute : str
    """
    if  _top_object.hasKey(_attribute):
        # check if callable
        return cs__is_callable(_top_object.get(_attribute))

    # check prototype
    if  not cs__var_exists(_env, _top_object.type):
        return False
    
    _proto = cs__get_prototype(_env, _top_object.type)
    if  _proto.hasKey(_attribute):
        # check if callable
        return cs__is_callable(_proto.get(_attribute))

    return False


def cs__get_attribute(_env:CSXEnvironment, _top_object:CSObject, _attr:str):
    """ Returns attribute of an object, otherwise error

        Parameters
        ----------
        _env : CSXEnvironment
        _top_object : CSObject
        _attr : str
    """  
    assert cs__has_attribute(_env, _top_object, _attr), "no attribute %s" % _attr

    # check has attribute
    if  _top_object.hasKey(_attr):
        return _env.stack.push(_top_object.get(_attr))

    _prototype = cs__get_prototype(_env, _top_object.type)
    if   _prototype.hasKey(_attr):
        return _env.stack.push(_prototype.get(_attr))



def cs__get_method(_env:CSXEnvironment, _top_object:CSObject, _attr:str):
    """ Get specific method of a type

        Parameters
        ----------
        _env : CXEnvironment
        _top_object : CSObject
        _attr : str
    """
    assert cs__has_method(_env, _top_object, _attr), "no method %s" % _attr

    # set this
    _env.current = _top_object

    # check proto
    cs__get_variable(_env, _top_object.type)
    
    _env.stack.push(_env.stack.poll().get(_attr))


def cs__set_attribute(_env:CSXEnvironment, _attr:str):
    """ Sets object attribute

        Parameters
        ----------
        _env : CXEnvironment
        _attr : str
    """
    if cs__has_method(_env, _env.stack.peek(), _attr):\
    logger("cs__set_attribte", "overriding native \"%s::%s\" method..." % (_env.stack.peek().type, _attr))

    # set current object
    _top_object = _env.stack.poll()
    _top_object.put(_attr, _env.stack.poll())









# 
def cs__construct_class(_env:CSXEnvironment, _arg_count:int):
    """ Creates a new class when unary "new"

        Parameters
        ----------
        _env : CXEnvironment
        _arg_count : int
    """
    _class_proto = _env.stack.poll()

    _new = _env.vheap.cs__malloc(CSObject())
    _new.type = _class_proto.type

    _keys = _class_proto.keys()
    for _k in _keys:
        # make a copy for non function
        if  not cs__is_callable(_class_proto.get(_k)):
            _new.put(_k, _class_proto.get(_k))

    _env.scope.append(Scope(_parent=_env.scope[-1]))

    cs__define_prop(_env, "this", _new)

    if  _class_proto.hasKey(_class_proto.type):
        _constructor = _class_proto.get(_class_proto.type)
        cs__raw_call(_env, _constructor, _arg_count)

    if  _constructor.type != CSTypes.TYPE_CSNATIVEFUNCTION:
        # hack!!!
        _env.stack.poll() # pop defult return
   
        # push newly created!
        _env.stack.push(_new)

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
        _ipointer   += 1

        match _instruction.opcode:

            case CSOpCode.PUSH_INTEGER:cs__new_number(_env, _instruction.get("const"))
            case CSOpCode.PUSH_DOUBLE:cs__new_number(_env, _instruction.get("const"))
            case CSOpCode.PUSH_STRING:cs__new_string(_env, _instruction.get("const"))
            case CSOpCode.PUSH_BOOLEAN:cs__new_boolean(_env, _instruction.get("const"))
            case CSOpCode.PUSH_NULL:cs__new_null(_env)
            case CSOpCode.PUSH_CODE:cs__new_code(_env, _instruction.get("code"))
            case CSOpCode.MAKE_FUNCTION:cs__new_function(_env)
            case CSOpCode.MAKE_CLASS:cs__new_class(_env, _instruction.get("size"))
            case CSOpCode.PUSH_NAME:
                _var_name = _instruction.get("name")
                if  not (cs__var_exists(_env, _var_name) or cs__local_exists(_env, _var_name)):
                    cs__error(
                        _env, ("ReferenceError: %s  is not defined!" % _var_name), 
                        _instruction.get("loc")
                    )
                    continue

                ######## get var|get local
                cs__get_variable(_env, _var_name)






            # event
            case CSOpCode.CALL:
                if  not cs__is_callable(_env.stack.peek()):
                    cs__error(
                        _env, ("TypeError: %s (%s) is not callable!" % (_env.stack.peek().type, _env.stack.peek().__str__())), 
                        _instruction.get("loc")
                    )
                    continue

                _name = _env.stack.peek().get("name")
                _argc = _env.stack.peek().get("argc")

                _passed_argument_size = _instruction.get("size")
                if  _argc.this != _passed_argument_size:
                    cs__error(
                        _env, ("TypeError: %s (%s) requires %s argument(s), got %d" % (_env.stack.peek().type, _name.__str__(), _argc.__str__(), _passed_argument_size)), 
                        _instruction.get("loc")
                    )
                    continue

                ######## call
                cs__call_function(_env, _env.stack.poll(), _passed_argument_size)

            case CSOpCode.CALL_METHOD:
                if  not cs__is_callable(_env.stack.peek()):
                    cs__error(
                        _env, ("TypeError: %s (%s) is not callable!" % (_env.stack.peek().type, _env.stack.peek().__str__())), 
                        _instruction.get("loc")
                    )
                    continue
                
                _name = _env.stack.peek().get("name")
                _argc = _env.stack.peek().get("argc")

                _passed_argument_size = _instruction.get("size")
                if  _argc.this != _passed_argument_size:
                    cs__error(
                        _env, ("TypeError: %s (%s) requires %s argument(s), got %d" % (_env.stack.peek().type, _name.__str__(), _argc.__str__(), _passed_argument_size)), 
                        _instruction.get("loc")
                    )
                    continue

                ######## call
                cs__call_method(_env, _env.stack.poll(), _passed_argument_size)

            case CSOpCode.MAKE_VAR:
                _var_name = _instruction.get("name")
                if  cs__var_exists(_env, _var_name):
                    cs__error(
                        _env, ("NameError: %s was already defined!" % _var_name), 
                        _instruction.get("loc")
                    )
                    continue

                ######## global var
                cs__make_variable(_env, _var_name, _env.stack.poll())

            case CSOpCode.MAKE_LOCAL:
                _loc_name = _instruction.get("name")
                if  cs__var_exists(_env, _loc_name):
                    cs__error(
                        _env, ("NameError: %s was already defined!" % _loc_name), 
                        _instruction.get("loc")
                    )
                    continue

                ######## local var
                cs__make_local(_env, _instruction.get("name"), _env.stack.poll())


            # attributes
            case CSOpCode.GET_ATTRIB:
                _attribute = _instruction.get("attr")
                if  not cs__has_attribute(_env,_env.stack.peek(), _attribute):
                    cs__error(
                        _env, ("AttributeError: %s has no attribute %s!" % (_env.stack.peek().__str__(), _attribute)),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## get attribute
                cs__get_attribute(_env, _env.stack.poll(), _attribute)

            case CSOpCode.GET_METHOD:
                _attribute = _instruction.get("attr")
                if  not cs__has_method(_env,_env.stack.peek(), _attribute):
                    cs__error(
                        _env, ("AttributeError: %s has no attribute %s!" % (_env.stack.peek().__str__(), _attribute)),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## get method
                cs__get_method(_env, _env.stack.poll(), _attribute)

            case CSOpCode.SET_ATTRIB:
                cs__set_attribute(_env, _instruction.get("attr"))
              


            # postfix
            case CSOpCode.POSTFIX_OP:
                match _instruction.get("opt"):
                    case "++":
                        if  not cs__has_method(_env, _env.stack.peek(), "__inc__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) for left operand!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                            
                        _top = _env.stack.peek().this
                        
                        ######## invoke self __inc__ method
                        _a = _env.stack.poll()
                        cs__invoke_method(_env, _a, "__inc__", 0)

                        # pop incremented
                        _env.stack.poll()

                        # push old value
                        cs__new_number(_env, _top)
                    
                    case "--":
                        if  not cs__has_method(_env, _env.stack.peek(), "__dec__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) for left operand!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                            
                        _top = _env.stack.peek().this
                        
                        ######## invoke self __inc__ method
                        _a = _env.stack.poll()
                        cs__invoke_method(_env, _a, "__dec__", 0)

                        # pop decremented
                        _env.stack.poll()

                        # push old value
                        cs__new_number(_env, _top)

                    case _:
                        raise Exception("not implemented %s" % _instruction.get("opt"))

            # unary
            case CSOpCode.UNARY_OP:
                match _instruction.get("opt"):
                    case "new":
                        """ A class/constructor must have an "attribute" named to itself.
                        """
                        if  not _env.stack.peek().hasKey(_env.stack.peek().type):
                            cs__error(
                                _env, ("TypeError: %s is not a constructor !" % _env.stack.peek().__str__()),
                                _instruction.get("loc")
                            )
                            continue

                        ######## construct class
                        cs__construct_class(_env, _instruction.get("size"))
                    
                    case "~":
                        _a = _env.stack.poll()
                        if  not cs__has_method(_env, _a, "__bit_not__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __bit_not__ method
                        cs__invoke_method(_env, _a, "__bit_not__", 0)
                    
                    case "!":
                        _a = _env.stack.poll()
                        if  not cs__has_method(_env, _a, "__log_not__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __log_not__ method
                        cs__invoke_method(_env, _a, "__log_not__", 0)
                    
                    case "+":
                        if  not cs__has_method(_env, _env.stack.peek(), "__uplus__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) for right operand!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __uplus__ method
                        _a = _env.stack.poll()
                        cs__invoke_method(_env, _a, "__uplus__", 0)

                    case "++":
                        if  not cs__has_method(_env, _env.stack.peek(), "__inc__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) for right operand!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __inc__ method
                        _a = _env.stack.poll()
                        cs__invoke_method(_env, _a, "__inc__", 0)
                    
                    case "-":
                        if  not cs__has_method(_env, _env.stack.peek(), "__uminus__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) for right operand!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __uminus__ method
                        _a = _env.stack.poll()
                        cs__invoke_method(_env, _a, "__uminus__", 0)

                    case "--":
                        if  not cs__has_method(_env, _env.stack.peek(), "__dec__"):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) for right operand!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __dec__ method
                        _a = _env.stack.poll()
                        cs__invoke_method(_env, _a, "__dec__", 0)
                    
                    case _:
                        raise Exception("not implemented %s" % _instruction.get("opt"))

            # multiplicative
            case CSOpCode.BINARY_POW:
                _a = _env.stack.poll()
                _pow_method = "__pow_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _pow_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __pow_RHS__ method
                cs__invoke_method(_env, _a, _pow_method, 1)

            case CSOpCode.BINARY_MUL:
                _a = _env.stack.poll()
                _mul_method = "__mul_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _mul_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __mul_RHS__ method
                cs__invoke_method(_env, _a, _mul_method, 1)
                
            case CSOpCode.BINARY_DIV:
                _a = _env.stack.poll()
                _div_method = "__div_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _div_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __div_RHS__ method
                cs__invoke_method(_env, _a, _div_method, 1)

            case CSOpCode.BINARY_MOD:
                _a = _env.stack.poll()
                _mod_method = "__mod_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _mod_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __mod_RHS__ method
                cs__invoke_method(_env, _a, _mod_method, 1)



            # addetive
            case CSOpCode.BINARY_ADD:
                _a = _env.stack.poll()
                _add_method = "__add_" + _env.stack.peek().type + "__"
               
                if  not cs__has_method(_env, _a, _add_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __add_RHS__ method
                cs__invoke_method(_env, _a, _add_method, 1)
            
            case CSOpCode.BINARY_SUB:
                _a = _env.stack.poll()
                _sub_method = "__sub_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _sub_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __sub_RHS__ method
                cs__invoke_method(_env, _a, _sub_method, 1)
            
            case CSOpCode.BINARY_LSHIFT:
                _a = _env.stack.poll()
                _lshift_method = "__lshift_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _lshift_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __lshift_RHS__ method
                cs__invoke_method(_env, _a, _lshift_method, 1)
            
            case CSOpCode.BINARY_RSHIFT:
                _a = _env.stack.poll()
                _rshift_method = "__rshift_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _rshift_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __rshift_RHS__ method
                cs__invoke_method(_env, _a, _rshift_method, 1)
            
            # comparison
            case CSOpCode.COMPARE_OP:
                match _instruction.get("opt"):
                    case "<":
                        _a = _env.stack.poll()
                        _lt_method = "__lt_" + _env.stack.peek().type + "__"
                        if  not cs__has_method(_env, _a, _lt_method):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __lt_RHS__ method
                        cs__invoke_method(_env, _a, _lt_method, 1)
                    
                    case "<=":
                        _a = _env.stack.poll()
                        _lte_method = "__lte_" + _env.stack.peek().type + "__"
                        if  not cs__has_method(_env, _a, _lte_method):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __lte_RHS__ method
                        cs__invoke_method(_env, _a, _lte_method, 1)
                    
                    case ">":
                        _a = _env.stack.poll()
                        _gt_method = "__gt_" + _env.stack.peek().type + "__"
                        if  not cs__has_method(_env, _a, _gt_method):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __gt_RHS__ method
                        cs__invoke_method(_env, _a, _gt_method, 1)
                    
                    case ">=":
                        _a = _env.stack.poll()
                        _gte_method = "__gte_" + _env.stack.peek().type + "__"
                        if  not cs__has_method(_env, _a, _gte_method):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __gte_RHS__ method
                        cs__invoke_method(_env, _a, _gte_method, 1)

                    case "==":
                        _a = _env.stack.poll()
                        _eq_method = "__eq_" + _env.stack.peek().type + "__"
                        if  not cs__has_method(_env, _a, _eq_method):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __eq_RHS__ method
                        cs__invoke_method(_env, _a, _eq_method, 1)
                    
                    case "!=":
                        _a = _env.stack.poll()
                        _neq_method = "__neq_" + _env.stack.peek().type + "__"
                        if  not cs__has_method(_env, _a, _neq_method):
                            cs__error(
                                _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                                _instruction.get("loc")
                            )
                            continue
                        
                        ######## invoke self __neq_RHS__ method
                        cs__invoke_method(_env, _a, _neq_method, 1)
            
            # bitwise logics
            case CSOpCode.BINARY_AND:
                _a = _env.stack.poll()
                _and_method = "__and_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _and_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __and_RHS__ method
                cs__invoke_method(_env, _a, _and_method, 1)
            
            case CSOpCode.BINARY_XOR:
                _a = _env.stack.poll()
                _xor_method = "__xor_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _xor_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __xor_RHS__ method
                cs__invoke_method(_env, _a, _xor_method, 1)
            
            case CSOpCode.BINARY_OR:
                _a = _env.stack.poll()
                _or_method = "__or_" + _env.stack.peek().type + "__"
                if  not cs__has_method(_env, _a, _or_method):
                    cs__error(
                        _env, ("TypeError: invalid operation (%s) of operands!" % _instruction.get("opt")),
                        _instruction.get("loc")
                    )
                    continue
                
                ######## invoke self __or_RHS__ method
                cs__invoke_method(_env, _a, _or_method, 1)
            

            # simple assignment
            case CSOpCode.STORE_NAME:
                _var_name = _instruction.get("name")
                if  not (cs__var_exists(_env, _var_name) or cs__local_exists(_env, _var_name)):
                    cs__error(
                        _env, ("NameError: %s is not defined!" % _var_name),
                        _instruction.get("loc")
                    )
                    continue

                ######## store var
                cs__store_name(_env, _var_name, _env.stack.poll())
            
            case CSOpCode.DUP_TOP:
                _env.stack.push(_env.stack.peek())

            case CSOpCode.PRINT_OBJECT:
                _size = _instruction.get("size")
                _format = ""

                for idx in range(_size):
                    _current = _env.stack.poll()
                    _string  = ""

                    if  cs__has_method(_env, _current, "__toString__"):
                        cs__invoke_method(_env, _current, "__toString__", 0)
                        _string = _env.stack.poll().__str__()
                    
                    else:
                        _string = _current.__str__()

                    _format += _string

                    if  idx < _size - 1:
                        _format += " "
                
                print(_format)

            case CSOpCode.POP_TOP:
                _env.stack.poll()

            case CSOpCode.RETURN_OP:
                return

            case _:
                raise NotImplementedError("invalid opcode %s" % _instruction.opcode.name)
    
    print("DONE!")


def cs__init_builtin(_env:CSXEnvironment):
    """
    """
    # linkage

    for each_class in ln:
        each_class().link([_env])

def cs__run(_code:csrawcode):
    _env = CSXEnvironment()

    # initialize before run
    cs__init_builtin(_env)

    # call module
    cs__call(_env, _code)




