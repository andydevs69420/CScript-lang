
from sys import exit
from enum import Enum
from gc import collect

# compiler
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
from csbuiltins import CSNullType
from csbuiltins import CSHashMap
from csbuiltins import CSMethod
from csbuiltins import CSNativeFunction
from csbuiltins import CSFunction

# utility
from utility import __throw__
from utility import logger


__ATTRIBUTE_INITIALIZE__ = "initialize"
__ATTRIBUTE___QUALNAME__ = "qualname"
__ATTRIBUTE__PROTOTYPE__ = "__proto__"


class SpecialAttrib(Enum):
    A =__ATTRIBUTE___QUALNAME__
    B =__ATTRIBUTE_INITIALIZE__
    C =__ATTRIBUTE__PROTOTYPE__


class CSXEnvironment(object):
    """ environment while running
    """

    # NEW!!! intead of using magic number
    MAX_CALL_STACK = 2000

    def __init__(self):
        self.scope = [Scope()]   # global scope
        self.vheap = VHEAP(self) # virtual heap
        self.stack = STACK()     # evaluation stack
        self.calls = STACK()     # callstack
        


class STACK(object):

    def __init__(self):
        self.__internal = [
        ]
    
    def push(self, _any):
        self.__internal.append(_any)

    def pop(self):
        return self.__internal.pop()
    
    def top(self):
        return self.__internal[-1]
    
    def all(self):
        return self.__internal
    
    def size(self):
        return len(self.__internal)


class VHEAP(object):
    """ Serves as heap memory
    """

    # NEW!!! intead of using magic number
    ALLOCATION_SIZE = 500

    def __init__(self, _env:CSXEnvironment):
        self.__bucket = []
        # unused index
        self.__unused = []
        self.__scopes = _env.scope

        self.__allocation = 0
    
    def cs__malloc(self, _csobject:CSObject):
        self.__on_allocate()
        
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
    
    def __on_allocate(self):
        self.__allocation += 1

        if  self.__allocation >= VHEAP.ALLOCATION_SIZE:
            self.collect()
            self.__allocation = 0

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
    
    def delete(self, _symbol:str):
        del self.symbols[_symbol]
    
    def update(self, _symbol:str, **_props):
        assert self.exists(_symbol, False), "null possibility not handled!"
        self.lookup(_symbol).update(_props)
    
    def lookup(self, _symbol:str):
        assert self.exists(_symbol, False), "null possibility not handled '%s'!" % _symbol
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


class CallFrame(object):
    """ Serves as StackFrame in callstack

        Parameters
        ----------
        _csrawcode : csrawcode
    """ 

    def __init__(self, _csrawcode:csrawcode, _global_scope:Scope):
        self.pointer = 0
        self.rawcode = _csrawcode
        self.locvars = [Scope(_parent=_global_scope)]
    
    def __str__(self):
        return "[csrawcode :pointer=%d]" % self.pointer


""" Begin runtime functions
"""


def cs__error(_env:CSXEnvironment, _message:str, _location:str):
    """ ThrowsError or flush to try/except

        Parameters
        ----------
        _env : CSXEnvironment
        _message : str
        _location : str
    """
    return __throw__(
        _message
        + "\n"
        + _location
    )

def cs_format_name_error_0(_env:CSXEnvironment, _name:str):
    """ Formats name error message if not defined!

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        str
    """
    return "ReferenceError: name '%s' is not defined in scope !!!" % _name


def cs_format_name_error_1(_env:CSXEnvironment, _name:str):
    """ Formats name error message if defined!

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        str
    """
    return "NameError: name '%s' was already defined in scope !!!" % _name


def cs_format_name_error_2(_env:CSXEnvironment, _name:str):
    """ Formats name error message if reassign without defining

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        str
    """
    return "NameError: re-assignment of '%s' without declairation !!!" % _name


def cs_format_att_error_0(_env:CSXEnvironment, _obj:CSObject, _attribute:str):
    """ Formats attribute error message

        Parameters
        ----------
        _env : CSXEnvironment
        _func : CSObject
        _attribute : str

        Returns
        -------
        str
    """
    return "AttributeError: missing attribute %s::%s !!!" % (_obj.type, _attribute)

def cs_format_att_error_1(_env:CSXEnvironment, _obj:CSObject, _attribute:str):
    """ Formats attribute error message

        Parameters
        ----------
        _env : CSXEnvironment
        _func : CSObject
        _attribute : str

        Returns
        -------
        str
    """
    return "AttributeError: trying to set a read-only attribute %s::%s !!!" % (_obj.type, _attribute)

def cs_format_method_error(_env:CSXEnvironment, _obj:CSObject, _attribute:str):
    """ Formats attribute error message

        Parameters
        ----------
        _env : CSXEnvironment
        _func : CSObject
        _attribute : str

        Returns
        -------
        str
    """
    return "AttributeError: missing method %s::%s !!!" % (_obj.type, _attribute)

def cs_format_not_callable_error(_env:CSXEnvironment, _obj:CSObject):
    """ Formats argument error message

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject

        Returns
        -------
        str
    """
    return "TypeError: %s is not callable !!!" % _obj.type

def cs_format_arg_error(_env:CSXEnvironment, _func:CSObject, _arg_size:int):
    """ Formats argument error message

        Parameters
        ----------
        _env : CSXEnvironment
        _func : CSObject
        _arg_size : int

        Returns
        -------
        str
    """
    _fname = _func.get("name").__str__()
    _fargc = _func.get("argc").__str__()
    return "ArgumentError: %s expected arg count %s, got %d !!!" % (_fname, _fargc, _arg_size)


def cs_format_post_type_error(_env:CSXEnvironment, _opt:str, _lhs:CSObject):
    """ Formats type error message for postfix expression

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _lhs : CSObject

        Returns
        -------
        str
    """
    return "TypeError: invalid postfix operator (%s) for type %s !!!" % (_opt, _lhs.type)

def cs_format_not_constructor_error(_env:CSXEnvironment, _obj:CSObject):
    """ Formats constructor error

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject

        Returns
        -------
        str
    """
    return "TypeError: %s is not a constructor !!!" % (_obj.type)

def cs_format_una_type_error(_env:CSXEnvironment, _opt:str, _rhs:CSObject):
    """ Formats type error message for unary expression

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _rhs : CSObject

        Returns
        -------
        str
    """
    return "TypeError: invalid unary operator (%s) for type %s !!!" % (_opt, _rhs.type)


def cs_format_bin_type_error(_env:CSXEnvironment, _opt:str, _lhs:CSObject, _rhs:CSObject):
    """ Formats type error message for binary expression

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _lhs : CSObject
        _rhs : CSObject

        Returns
        -------
        str
    """
    return "TypeError: invalid operator (%s) for operands type %s and %s !!!" % (_opt, _lhs.type, _rhs.type)


def cs_format_zero_division_error(_env:CSXEnvironment, _opt:str, _lhs:CSObject, _rhs:CSObject):
    """ Formats type error message for zero division

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _lhs : CSObject
        _rhs : CSObject

        Returns
        -------
        str
    """
    return "ZeroDivisionError: divisor of dividend produces zero !!!"

def cs_format_thrown_error(_env:CSXEnvironment, _obj:CSObject):
    """ Formats type error message for zero division

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject

        Returns
        -------
        str
    """
    _err = ...
    if  cs_has_method(_env, _obj, "toString"):
        _err = cs_invoke_method(_env, _obj, "toString", 0).__str__()
    else:
        _err = _obj.__str__()
    return _err



"""OPCODE INJECTION"""
def cs_rot_2(_env:CSXEnvironment):
    """ Rotates 2 object in stack

        Parameters
        ----------
        _env:CSXEnvironment
    """
    _top = _env.stack.pop()
    _nxt = _env.stack.pop()

    _env.stack.push(_top)
    _env.stack.push(_nxt)


def cs_execute(_env:CSXEnvironment, _once:bool=False):
    
    while _env.calls.size() > 0:
        
        ### TOP CALLSTACK CODE!!
        _rawcode:CallFrame = _env.calls.top()

        # for i in _rawcode.rawcode:
        #     print(i)

        while _rawcode.pointer < len(_rawcode.rawcode):

            _opc:Instruction = _rawcode.rawcode.code[_rawcode.pointer]
            _rawcode.pointer += 1
            
            match _opc.opcode:

                case CSOpCode.PUSH_CODE:
                    """"""
                    cs_new_code(_env, _opc.get("code"))

                case CSOpCode.PUSH_INTEGER:
                    """"""
                    cs_new_number(_env, _opc.get("const"))

                case CSOpCode.PUSH_DOUBLE:
                    """"""
                    cs_new_number(_env, _opc.get("const"))
                
                case CSOpCode.PUSH_STRING:
                    """"""
                    cs_new_string(_env, _opc.get("const"))
                
                case CSOpCode.PUSH_BOOLEAN:
                    """"""
                    cs_new_boolean(_env, _opc.get("const"))
                
                case CSOpCode.PUSH_NULL:
                    """"""
                    cs_new_nulltype(_env)
                
                case CSOpCode.MAKE_OBJECT:
                    """"""
                    cs_new_object(_env, _opc.get("size"))

                case CSOpCode.PUSH_NAME:
                    """"""
                    _name = _opc.get("name")

                    if  not cs_has_var(_env, _name):
                        cs__error(_env, cs_format_name_error_0(_env, _name), _opc.get("loc"))
                        continue
                        
                    #####
                    cs_push_name(_env, _name)
                

                case CSOpCode.GET_ATTRIB:
                    """"""
                    if  not cs_has_attribute(_env, _env.stack.top(), _opc.get("attr")):
                        cs__error(_env, cs_format_att_error_0(_env, _env.stack.top(), _opc.get("attr")), _opc.get("loc"))
                        continue

                    #####
                    cs_get_attrib(_env, _opc.get("attr"))
                
                case CSOpCode.SET_ATTRIB:
                    """"""
                    # allow making an attribute!!
                    
                    match _opc.get("attr"):

                        case SpecialAttrib.A.value|\
                             SpecialAttrib.B.value|\
                             SpecialAttrib.C.value:
                            # As for the moment, we cant freeze object!!
                            cs__error(_env, cs_format_att_error_1(_env, _env.stack.top(), _opc.get("attr")), _opc.get("loc"))
                            continue

                        case _:
                            #####
                            cs_set_attrib(_env, _opc.get("attr"))
                
                case CSOpCode.GET_METHOD:
                    """"""
                    if  not cs_has_method(_env, _env.stack.top(), _opc.get("attr")):
                        cs__error(_env, cs_format_method_error(_env, _env.stack.top(), _opc.get("attr")), _opc.get("loc"))
                        continue

                    #####
                    cs_get_method(_env, _opc.get("attr"))
                
                case CSOpCode.CALL_METHOD:
                    """"""
                    if  _env.stack.top().get("argc").this != _opc.get("size"):
                        cs__error(_env, cs_format_arg_error(_env, _env.stack.top(), _opc.get("size")), _opc.get("loc"))
                        continue
                    
                    _copy = _env.stack.top()

                    #####
                    cs_method_call(_env, _opc.get("size"))

                    # request break when user defined method
                    if  cs_is_function(_copy):
                        break


                case CSOpCode.CALL:
                    """"""
                    if  not cs_is_callable(_env.stack.top()):
                        cs__error(_env, cs_format_not_callable_error(_env, _env.stack.top()), _opc.get("loc"))
                        continue

                    if  _env.stack.top().get("argc").this != _opc.get("size"):
                        cs__error(_env, cs_format_arg_error(_env, _env.stack.top(), _opc.get("size")), _opc.get("loc"))
                        continue
                    
                    _copy = _env.stack.top()

                    #####
                    cs_function_call(_env, _opc.get("size"))

                    # request break when user defined function
                    if  cs_is_function(_copy):
                        break
                

                case CSOpCode.POSTFIX_OP:
                    raise NotImplementedError("Not implemented op '%s' !!!" % _opc.get("opt"))
                    # match _opc.get("opt"):

                    #     case "++":
                    #         _top = _env.stack.pop()

                    #         if  not cs_is_number(_top):
                    #             cs__error(_env, cs_format_post_type_error(_env, _opc.get("opt"), _top), _opc.get("loc"))
                    #             continue
                        
                    #         #####
                    #         # push old
                    #         cs_new_number(_env, _top.this)

                    #         # inc
                    #         _top.this += 1

                    #     case "--":
                    #         _top = _env.stack.pop()

                    #         if  not cs_is_number(_top):
                    #             cs__error(_env, cs_format_post_type_error(_env, _opc.get("opt"), _top), _opc.get("loc"))
                    #             continue
                        
                    #         #####
                    #         # push old
                    #         cs_new_number(_env, _top.this)

                    #         # dec
                    #         _top.this -= 1


                case CSOpCode.UNARY_OP:

                    match _opc.get("opt"):

                        case "new":
                            """"""
                            if  not cs_is_constructor(_env.stack.top()):
                                cs__error(_env, cs_format_not_constructor_error(_env, _env.stack.top()), _opc.get("loc"))
                                continue
                            
                            _copy = _env.stack.top()

                            # check arg
                            cs_get_attrib(_env, __ATTRIBUTE_INITIALIZE__)
                            
                            if  _env.stack.top().get("argc").this != _opc.get("size"):
                                cs__error(_env, cs_format_arg_error(_env, _env.stack.top(), _opc.get("size")), _opc.get("loc"))
                                continue
                            
                            # pop constructor
                            _env.stack.pop()
                            
                            # push top old
                            _env.stack.push(_copy)
                            
                            #####
                            cs_constructor(_env, _opc.get("size"))
                        
                        case "typeof":
                            """"""
                            cs_new_string(_env, _env.stack.pop().type)

                        case "!":
                            _rhs = _env.stack.pop()

                            #####
                            if  not cs_is_pointer(_rhs):
                                cs_new_boolean(_env, not _rhs.this)
                            else:
                                cs_new_boolean(_env, False)

                        case "~":
                            _rhs = _env.stack.pop()

                            if  not cs_is_integer(_rhs):
                                cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                                continue

                            #####
                            cs_new_number(_env, ~ _rhs.this)
                        

                        case "+":
                            _rhs = _env.stack.pop()

                            if  not cs_is_number(_rhs):
                                cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                                continue

                            #####
                            cs_new_number(_env, + _rhs.this)
                        

                        case "-":
                            _rhs = _env.stack.pop()

                            if  not cs_is_number(_rhs):
                                cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                                continue

                            #####
                            cs_new_number(_env, - _rhs.this)
                        

                        # case "++":
                        #     _rhs = _env.stack.pop()

                        #     if  not cs_is_number(_rhs):
                        #         cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        #         continue
                            
                        #     cs_new_number(_env, _rhs.this + 1)

                        #     #####
                        #     _rhs.this += 1

                        
                        # case "--":
                        #     _rhs = _env.stack.top()

                        #     if  not cs_is_number(_rhs):
                        #         cs__error(_env, cs_format_una_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        #         continue

                        #     #####
                        #     _rhs.this -= 1
                        case _:
                            raise NotImplementedError("Not implemented op '%s' !!!" % _opc.get("opt"))


                case CSOpCode.BINARY_POW:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    #####
                    cs_new_number(_env, _lhs.this ** _rhs.this)
                

                case CSOpCode.BINARY_MUL:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    #####
                    cs_new_number(_env, _lhs.this * _rhs.this)
                

                case CSOpCode.BINARY_DIV:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    # zero divisor
                    if  _rhs.this == 0:
                        cs__error(_env, cs_format_zero_division_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    #####
                    cs_new_number(_env, _lhs.this / _rhs.this)
                

                case CSOpCode.BINARY_MOD:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    # zero divisor
                    if  _rhs.this == 0:
                        cs__error(_env, cs_format_zero_division_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    #####
                    cs_new_number(_env, _lhs.this % _rhs.this)


                case CSOpCode.BINARY_ADD:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()
                
                    if  not ((cs_is_number(_lhs) and cs_is_number(_rhs)) or \
                            (cs_is_string(_lhs) and cs_is_string(_rhs))):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    if cs_is_number(_lhs) and cs_is_number(_rhs):
                        cs_new_number(_env, _lhs.this + _rhs.this)
                    else:
                        cs_new_string(_env, _lhs.this + _rhs.this)
                

                case CSOpCode.BINARY_SUB:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    #####
                    cs_new_number(_env, _lhs.this - _rhs.this)
                
                case CSOpCode.BINARY_LSHIFT:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not cs_is_integer(_lhs) and cs_is_integer(_rhs):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    #####
                    cs_new_number(_env, _lhs.this << _rhs.this)
                

                case CSOpCode.BINARY_RSHIFT:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not cs_is_integer(_lhs) and cs_is_integer(_rhs):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue

                    #####
                    cs_new_number(_env, _lhs.this >> _rhs.this)
                
                case CSOpCode.COMPARE_OP:
                    match _opc.get("opt"):

                        case "<":
                            _lhs = _env.stack.pop()
                            _rhs = _env.stack.pop()

                            if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                                cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                                continue

                            #####
                            cs_new_boolean(_env, _lhs.this < _rhs.this)
                        
                        case "<=":
                            _lhs = _env.stack.pop()
                            _rhs = _env.stack.pop()

                            if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                                cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                                continue

                            #####
                            cs_new_boolean(_env, _lhs.this <= _rhs.this)
                        

                        case ">":
                            _lhs = _env.stack.pop()
                            _rhs = _env.stack.pop()

                            if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                                cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                                continue

                            #####
                            cs_new_boolean(_env, _lhs.this > _rhs.this)
                        
                        case ">=":
                            _lhs = _env.stack.pop()
                            _rhs = _env.stack.pop()

                            if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                                cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                                continue

                            #####
                            cs_new_boolean(_env, _lhs.this >= _rhs.this)
                        
                        case "==":
                            _lhs = _env.stack.pop()
                            _rhs = _env.stack.pop()

                            if  not (cs_is_pointer(_lhs) or cs_is_pointer(_rhs)):
                                cs_new_boolean(_env, _lhs.this == _rhs.this)
                                continue
                        
                            ##### pointer: compare memory address
                            cs_new_boolean(_env, _lhs.offset == _rhs.offset)
                        

                        case "!=":
                            _lhs = _env.stack.pop()
                            _rhs = _env.stack.pop()

                            if  not (cs_is_pointer(_lhs) or cs_is_pointer(_rhs)):
                                cs_new_boolean(_env, _lhs.this != _rhs.this)
                                continue
                        
                            ##### pointer: compare memory address
                            cs_new_boolean(_env, _lhs.offset != _rhs.offset)
                        

                case CSOpCode.BINARY_AND:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this & _rhs.this)
                

                case CSOpCode.BINARY_XOR:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this ^ _rhs.this)
                

                case CSOpCode.BINARY_OR:
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this | _rhs.this)

                case CSOpCode.MAKE_CLASS:
                    """"""
                    cs_new_class(_env, _opc.get("size"))

                case CSOpCode.MAKE_FUNCTION:
                    """"""
                    cs_new_function(_env)

                case CSOpCode.MAKE_VAR:
                    """"""
                    if  cs_has_global(_env, _opc.get("name")):
                        cs__error(_env, cs_format_name_error_1(_env, _opc.get("name")), _opc.get("loc"))
                        continue

                    #####
                    cs_make_var(_env, _opc.get("name"))
                
                case CSOpCode.MAKE_LOCAL:
                    """"""
                    if  cs_has_local(_env, _opc.get("name")):
                        cs__error(_env, cs_format_name_error_1(_env, _opc.get("name")), _opc.get("loc"))
                        continue

                    #####
                    cs_make_local(_env, _opc.get("name"))
                
                case CSOpCode.STORE_NAME:
                    """"""
                    _name = _opc.get("name")

                    if  not cs_has_var(_env, _name):
                        cs__error(_env, cs_format_name_error_2(_env, _name), _opc.get("loc"))
                        continue

                    #####
                    cs_store_name(_env, _name)
                
                case CSOpCode.INPLACE_POW:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this ** _rhs.this)
                    
                
                case CSOpCode.INPLACE_MUL:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this * _rhs.this)
                
                case CSOpCode.INPLACE_DIV:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    # zero divisor
                    if  _rhs.this == 0:
                        cs__error(_env, cs_format_zero_division_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this / _rhs.this)
                
                case CSOpCode.INPLACE_MOD:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    # zero divisor
                    if  _rhs.this == 0:
                        cs__error(_env, cs_format_zero_division_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this % _rhs.this)

                case CSOpCode.INPLACE_ADD:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()
    
                    if  not ((cs_is_number(_lhs) and cs_is_number(_rhs)) or \
                             (cs_is_string(_lhs) and cs_is_string(_rhs))):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    if cs_is_number(_lhs) and cs_is_number(_rhs):
                        cs_new_number(_env, _lhs.this + _rhs.this)
                    else:
                        cs_new_string(_env, _lhs.this + _rhs.this)

                case CSOpCode.INPLACE_SUB:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this - _rhs.this)
                
                case CSOpCode.INPLACE_LSHIFT:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this << _rhs.this)
                
                case CSOpCode.INPLACE_RSHIFT:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this >> _rhs.this)
                
                case CSOpCode.INPLACE_AND:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this & _rhs.this)
                
                case CSOpCode.INPLACE_XOR:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this ^ _rhs.this)
                
                case CSOpCode.INPLACE_OR:
                    """"""
                    _lhs = _env.stack.pop()
                    _rhs = _env.stack.pop()

                    if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                        cs__error(_env, cs_format_bin_type_error(_env, _opc.get("opt"), _lhs, _rhs), _opc.get("loc"))
                        continue
                    
                    #####
                    cs_new_number(_env, _lhs.this | _rhs.this)
                

                case CSOpCode.POP_JUMP_IF_FALSE:
                    """"""
                    _top = _env.stack.pop()

                    if  cs_is_nulltype(_top) or cs_is_bool_false(_top):
                        _rawcode.pointer = _opc.get("target") // 2
                    
                    # print(_env.vheap.cs__object_at(_env.calls.top().locvars[-1].lookup("_head")["_address"]))
                
                case CSOpCode.POP_JUMP_IF_TRUE:
                    """"""
                    _top = _env.stack.pop()

                    if  not (cs_is_nulltype(_top) or cs_is_bool_false(_top)):
                        _rawcode.pointer = _opc.get("target") // 2
                

                case CSOpCode.JUMP_IF_TRUE_OR_POP:
                    """"""
                    _top = _env.stack.top()

                    if  (not cs_is_nulltype(_top)) or cs_is_bool_true(_top):
                        _rawcode.pointer = _opc.get("target") // 2
                        continue
                    
                    ##### pop
                    _env.stack.pop()


                case CSOpCode.JUMP_IF_FALSE_OR_POP:
                    """"""
                    _top = _env.stack.top()

                    if  cs_is_nulltype(_top) or cs_is_bool_false(_top):
                        _rawcode.pointer = _opc.get("target") // 2
                        continue
                    
                    ##### pop
                    _env.stack.pop()

                case CSOpCode.JUMP_EQUAL:
                    """"""
                    _a = _env.stack.pop()
                    _b = _env.stack.pop()

                    if  not (cs_is_pointer(_a) or cs_is_pointer(_b)):
                        if  _a.this == _b.this:
                            _rawcode.pointer = _opc.get("target") // 2
                    else:
                        if  _a.offset == _b.offset:
                            _rawcode.pointer = _opc.get("target") // 2

                case CSOpCode.ABSOLUTE_JUMP:
                    """"""
                    _rawcode.pointer = _opc.get("target") // 2
                

                case CSOpCode.JUMP_TO:
                    """"""
                    _rawcode.pointer = _opc.get("target") // 2
                

                case CSOpCode.DUP_TOP:
                    """"""
                    _env.stack.push(_env.stack.top())


                case CSOpCode.POP_TOP:
                    """"""
                    _env.stack.pop()

                
                case CSOpCode.PRINT_OBJECT:
                    """"""
                    _size = _opc.get("size")
                    _frmt = ""

                    for _r in range(_size):
                        
                        _top = _env.stack.pop()
                        _str = ""; 

                        if  cs_has_method(_env, _top, "toString") and not cs_is_string(_top):
                            _str += cs_invoke_method(_env, _top, "toString", 0).__str__()
                        else:
                            _str += _top.__str__()

                        _frmt += _str

                        if  _r < (_size - 1):
                            _frmt += " "
                    
                    print(_frmt)
                
                case CSOpCode.NEW_BLOCK:
                    """"""
                    cs_new_scope(_env)
                
                case CSOpCode.END_BLOCK:
                    """"""
                    cs_end_scope(_env)
                
                case CSOpCode.THROW_ERROR:
                    """"""
                    cs__error(_env, cs_format_thrown_error(_env, _env.stack.pop()), _opc.get("loc"))
                
                case CSOpCode.NO_OPERATION:
                    """"""
                    pass

                case CSOpCode.RETURN_OP:
                    """"""
                    _env.calls.pop()
                    break

                case _:
                    print("Not implemented opcode", _opc.opcode.name)
                    exit(1)

        if _once: break


"""HELPERS"""
def cs_ifdef(_env:CSXEnvironment, _name:str):
    """ Checks if name exists to local scope

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    return _env.calls.top().locvars[-1].exists(_name, _local=True)


def cs_has_var(_env:CSXEnvironment, _name:str):
    """ Checks if name exists in local->global scope

        Allow cascade search

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    if  _env.scope[-1].exists(_name, _local=False):
        return True
    #####
    return _env.calls.top().locvars[-1].exists(_name, _local=False)


def cs_has_global(_env:CSXEnvironment, _name:str):
    """ Checks if name exists in global scope

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    return _env.scope[-1].exists(_name, _local=False)


def cs_has_local(_env:CSXEnvironment, _name:str):
    """ Checks if name exists to local scope

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    return _env.calls.top().locvars[-1].exists(_name, _local=True)


def cs_has_class(_env:CSXEnvironment, _class_name:str):
    """ Checks if class exist

        Parameters
        ----------
        _env : CSXEnvironment
        _class_name : str

        Returns
        -------
        bool
    """
    _exist = _env.scope[-1].exists(_class_name, _local=False)
    if not _exist: return _exist

    # retirieve
    _infor = _env.scope[-1].lookup(_class_name)
   
    _class = _env.vheap.cs__object_at(_infor["_address"])
    
    # check if valid class
    return cs_is_constructor(_class)




def cs_has_method(_env:CSXEnvironment, _obj:CSObject, _method_name:str):
    """ Checks if _obj has _method_name to its class proto

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject
        _method_name : str

        Returns
        -------
        bool
    """
    # if contains "__proto__"
    if  not cs_has_attribute(_env, _obj, __ATTRIBUTE__PROTOTYPE__): 
        return False

    # search in class
    _class = _obj.get(__ATTRIBUTE__PROTOTYPE__)

    if  not cs_has_attribute(_env, _class, _method_name):
        return False

    return cs_is_callable(_class.get(_method_name))



def cs_has_attribute(_env:CSXEnvironment, _obj:CSObject, _attribute_name:str):
    """ Check if object has direct attribute/key

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject
        _method_name : str

        Returns
        -------
        bool
    """
    if  _obj.hasKey(_attribute_name):
        return True
    
    # search in prototype
    if  not _obj.hasKey(__ATTRIBUTE__PROTOTYPE__):
        return False
    
    _class = _obj.get(__ATTRIBUTE__PROTOTYPE__)

    return _class.hasKey(_attribute_name)


def cs_is_callable(_obj:CSObject|CSFunction|CSNativeFunction):
    """ Checks if object is a function

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject

        Returns
        -------
        bool
    """ 
    return (
        cs_is_native_function(_obj) or
        cs_is_function(_obj)        or
        cs_is_method(_obj)
    )

def cs_is_native_function(_csobject:CSObject):
    """ Checks if object is a native function

        Parameters
        ----------
        _csobject : CSObject
    """
    return _csobject.type == CSTypes.TYPE_CSNATIVEFUNCTION


def cs_is_function(_csobject:CSObject):
    """ Checks if object is a user function

        Parameters
        ----------
        _csobject : CSObject
    """
    return _csobject.type == CSTypes.TYPE_CSFUNCTION


def cs_is_method(_csobject:CSObject):
    """ Checks if object is a method

        Parameters
        ----------
        _csobject : CSObject
    """
    return _csobject.type == CSTypes.TYPE_CSMETHOD


def cs_is_rawcode(_csobject:CSObject):
    """ Checks if object is csrawcode

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSRAWCODE



def cs_is_number(_csobject:CSObject):
    """ Checks if object is CSInteger or CSDouble

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  cs_is_integer(_csobject) or cs_is_double(_csobject)


def cs_is_integer(_csobject:CSObject):
    """ Checks if object is CSInteger

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSINTEGER


def cs_is_double(_csobject:CSObject):
    """ Checks if object is CSDouble

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSDOUBLE


def cs_is_string(_csobject:CSObject):
    """ Checks if object is CSString

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  _csobject.type == CSTypes.TYPE_CSSTRING


def cs_is_boolean(_csobject:CSObject):
    """ Checks if object is CSBoolean

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return  _csobject.type == CSTypes.TYPE_CSBOOLEAN


def cs_is_bool_true(_csobject:CSObject):
    """ Checks if object is CSBoolean true

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    if  not cs_is_boolean(_csobject):
        return not cs_is_nulltype(_csobject)
    
    return _csobject.this


def cs_is_bool_false(_csobject:CSObject):
    """ Checks if object is CSBoolean false

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    
    return not cs_is_bool_true(_csobject)


def cs_is_nulltype(_csobject:CSObject):
    """ Checks if object is CSNullType

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSNULLTYPE


def cs_is_constructor(_csobject:CSObject):
    """ Checks if object is a constructor
        
        A valid class should have
            the following: 
            
            [1]. initialize method(CSCallable constructor)

            [2]. qualname attribute(CSString)

        so.. this is a valid class

            var MYCLASS = {
                qualname: "MyClass",
                initialize: function() {
                    
                }
            };

        
        Parameters
        ----------
        _env : CSXEnvironment
        _csobject : CSObject

        Returns
        -------
        bool
    """

    # check if object has "qualname"
    if  not _csobject.hasKey(__ATTRIBUTE___QUALNAME__):
        return False
    
    # is qualname a string?
    if  not cs_is_string(_csobject.get(__ATTRIBUTE___QUALNAME__)):
        # invalid qualname
        return False
    
    # has qualname!

    # check if has "initialize" method
    if  not _csobject.hasKey(__ATTRIBUTE_INITIALIZE__):
        # no valid constructor
        return False
    
    # is constructor callable?
    return cs_is_callable(_csobject.get(__ATTRIBUTE_INITIALIZE__))


def cs_is_pointer(_csobject:CSObject):
    """ Checks if object is a pointer type

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return not (cs_is_number(_csobject) or cs_is_string(_csobject) or cs_is_boolean(_csobject) or cs_is_nulltype(_csobject))


"""OPCODE METHODS"""
def cs_define(_env:CSXEnvironment, _name:str, _value:CSObject):
    """ Creates local variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
        _value : CSObject
    """
    assert not cs_ifdef(_env, _name), "name '%s' already defined!" % _name

    # save var
    _env.calls.top().locvars[-1].insert(_name, _address=_value.offset, _global=False)


def cs_undefine(_env:CSXEnvironment, _name:str):
    """ Removes local variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert cs_ifdef(_env, _name), "name '%s' is not defined!" % _name

    # save var
    _env.calls.top().locvars[-1].delete(_name)

def cs_make_var(_env:CSXEnvironment, _name:str):
    """ Creates global variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert not cs_has_global(_env, _name), "name '%s' already defined!" % _name

    # save var
    _env.scope[-1].insert(_name, _address=_env.stack.pop().offset, _global=True)


def cs_make_local(_env:CSXEnvironment, _name:str):
    """ Creates local variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert not cs_has_local(_env, _name), "name '%s' already defined!" % _name

    # save var
    _env.calls.top().locvars[-1].insert(_name, _address=_env.stack.pop().offset, _global=False)


def cs_store_name(_env:CSXEnvironment, _name:str):
    """ Reassign variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert cs_has_var(_env, _name), "no such name '%s'" % _name

    if  _env.scope[-1].exists(_name, _local=False):
        #### search globally
        _env.scope[-1].update(_name, _address=_env.stack.pop().offset)
    else:
        #### search locally
        _env.calls.top().locvars[-1].update(_name, _address=_env.stack.pop().offset)


def cs_new_code(_env:CSXEnvironment, _raw_code:csrawcode):
    """ Push number to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _raw_code : csrawcode
    """ 
    _env.stack.push(_env.vheap.cs__malloc(_raw_code))


def cs_new_number(_env:CSXEnvironment, _py_number:int|float):
    """ Push number to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_number : int|float
    """ 
    _obj = None
    if  type(_py_number) == int:
        _obj = _env.vheap.cs__malloc(CSInteger(_py_number))

    else:
        _obj = _env.vheap.cs__malloc(CSDouble (_py_number))

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())
   

    # push #
    _env.stack.push(_obj)



def cs_new_string(_env:CSXEnvironment, _py_string:str):
    """ Push string to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_string : str
    """ 

    _obj = CSString(_py_string)

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())

    _env.stack.push(_env.vheap.cs__malloc(_obj))


def cs_new_boolean(_env:CSXEnvironment, _py_boolean:bool):
    """ Push boolean to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_boolean : bool
    """ 

    _obj = CSBoolean(_py_boolean)

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())

    _env.stack.push(_env.vheap.cs__malloc(_obj))



def cs_new_nulltype(_env:CSXEnvironment):
    """ Push boolean to stack

        Parameters
        ----------
        _env : CSXEnvironment
    """ 

    _obj = CSNullType()

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())

    _env.stack.push(_env.vheap.cs__malloc(_obj))


def cs_new_object(_env:CSXEnvironment, _pop_size:int):
    """ Push boolean to stack

        Parameters
        ----------
        _env : CSXEnvironment
    """ 

    _obj = CSHashMap()

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())
    

    for _r in range(_pop_size):
        _key = _env.stack.pop()
        _val = _env.stack.pop()
        _obj.put(_key.__str__(), _val)

    _env.stack.push(_env.vheap.cs__malloc(_obj))


def cs_new_class(_env:CSXEnvironment, _pop_size:int):
    """ Push/Builds a class prototype

        Parameters
        ----------
        _env : CSXEnvironment
        _pop_size : int
    """
    _class_proto_name = _env.stack.pop()

    # creates new object as class proto
    _obj = _env.vheap.cs__malloc(CSObject())

    # set qualifed name
    _obj.put(__ATTRIBUTE___QUALNAME__, _class_proto_name)

    for _r in range(_pop_size):
        _key = _env.stack.pop()
        _val = _env.stack.pop()
        # put object
        _obj.put(_key.__str__(), _val)
    
    _env.stack.push(_obj)


def cs_new_function(_env:CSXEnvironment):
    """ Push/Builds a function

        Parameters
        ----------
        _env : CSXEnvironment
    """
    _fname = _env.stack.pop()
    _fargc = _env.stack.pop()
    _fcode = _env.stack.pop()

    _obj = CSFunction(_fname, _fargc, _fcode)
    
    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())


    _env.stack.push(_env.vheap.cs__malloc(_obj))



def cs_push_name(_env:CSXEnvironment, _name:str):
    """ Gets variable value

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert cs_has_var(_env, _name), "no such name '%s'" % _name

    # retrieve starts from local to global
    _info = ...

    if  _env.scope[-1].exists(_name, _local=False):
        #### search globally
        _info = _env.scope[-1].lookup(_name)
    else:
        #### search locally
        _info = _env.calls.top().locvars[-1].lookup(_name)
    
    # push stack
    _env.stack.push(_env.vheap.cs__object_at(_info["_address"]))



def cs_get_class(_env:CSXEnvironment, _class_name:str):
    """ Retrievs class prototype

        Parameters
        ----------
        _env : CSXEnvironment
        _class_name : str
    """
    assert cs_has_class(_env, _class_name), "No such class" % _class_name

    # retrieve
    _info = _env.scope[-1].lookup(_class_name)
    
    # push stack
    _env.stack.push(_env.vheap.cs__object_at(_info["_address"]))


"""MEMBER"""

def cs_get_attrib(_env:CSXEnvironment, _attribute_name:str):
    """ Gets attribute of an object

        Parameters
        ----------
        _env : CSXEnvironment
        _attribute_name : str
    """
    assert cs_has_attribute(_env, _env.stack.top(), _attribute_name), "No such attribute '%s'" % _attribute_name

    _top = _env.stack.pop()
    if  _top.hasKey(_attribute_name):
        _env.stack.push(_top.get(_attribute_name))
        return 
    
    # search in class
    _class = _top.get(__ATTRIBUTE__PROTOTYPE__)

    # push to stack
    _env.stack.push(_class.get(_attribute_name))



def cs_get_method(_env:CSXEnvironment, _method_name:str):
    """ Extracts method from class prototype

        Parameters
        ----------
        _env : CSXEnvironment
        _method_name : str
        
    """
    assert cs_has_method(_env, _env.stack.top(), _method_name), "No such method '%s'" % _method_name

    # top object
    _objct = _env.stack.pop()
    
    # class becomes __proto__
    _class = _objct.get(__ATTRIBUTE__PROTOTYPE__)

    # push to stack
    _env.stack.push(_env.vheap.cs__malloc(CSMethod(_objct, _class.get(_method_name))))


def cs_set_attrib(_env:CSXEnvironment, _attribute_name:str):
    """ Sets attribute of an object

        Parameters
        ----------
        _env : CSXEnvironment
        _attribute_name : str
    """
    _obj = _env.stack.pop()
    _obj.put(_attribute_name, _env.stack.pop())
    

"""FUNCTIONS"""
def cs_method_call(_env:CSXEnvironment, _argument_size:int):
    """ Calls a method

        Parameters
        ----------
        _env : CSXEnvironment
        _argument_size : int
    """
    assert cs_is_callable(_env.stack.top()), "not a function!"

    #   stack
    # ---------
    #  method
    #  args 0
    #  args N

    # method
    _func = _env.stack.pop()

    match _func.meth:
        
        case CSTypes.TYPE_CSNATIVEFUNCTION:
            # call function
            _args = [_env]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())
            
            # add native scope
            cs_new_scope(_env)

            # define "this"
            cs_define(_env, "this", _func.get("owner"))

            _env.stack.push(_func.call(_args))

            # remove this from scope
            cs_undefine(_env, "this")

            # pop native scope
            cs_end_scope(_env)

        case CSTypes.TYPE_CSFUNCTION:
            # call function
            cs_call(_env, _func.get("code"))
    
            # define "this"
            cs_define(_env, "this", _func.get("owner"))


def cs_function_call(_env:CSXEnvironment, _argument_size:int):
    """ Calls a function

        Parameters
        ----------
        _env : CSXEnvironment
        _argument_size : int
    """
    #   stack
    # ---------
    #  method
    #  args 0
    #  args N

    assert cs_is_callable(_env.stack.top()), "not a function!"

    # method
    _func = _env.stack.pop()

    match _func.type:
        case CSTypes.TYPE_CSNATIVEFUNCTION:
            # call function
            _args = [_env]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())
            
            # add native scope
            cs_new_scope(_env)

            _env.stack.push(_func.call(_args))

            # pop native scope
            cs_end_scope(_env)

        case CSTypes.TYPE_CSFUNCTION:
            # call function
            cs_call(_env, _func.get("code"))



def cs_invoke_method(
    _env : CSXEnvironment,
    _obj : CSObject,
    _method_name : str,
    _argument_size : int
):
    """ Invokes internal method and return

        # NOTE: caller should pop!!!

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject
        _method_name : str
        _argument_size : int

        Returns
        -------
        CSOject
    """
    assert cs_has_method(_env, _obj, _method_name), "No such method '%s'" % _method_name

    # NOTE: caller should pop!!!
    # push back to stack
    _env.stack.push(_obj)
    
    # push method to stack
    cs_get_method(_env, _method_name)
    
    # request call
    _func = _env.stack.pop()

    match _func.meth:

        case CSTypes.TYPE_CSNATIVEFUNCTION:
            # call function
            _args = [_env]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())

            # add native scope
            cs_new_scope(_env)

            # define "this"
            cs_define(_env, "this", _func.get("owner"))
            
            _env.stack.push(_func.call(_args))

            # remove this from scope
            cs_undefine(_env, "this")

            # pop native scope
            cs_end_scope(_env)

        case CSTypes.TYPE_CSFUNCTION:
            # call function
            cs_call(_env, _func.get("code"))
            
            # define "this"
            cs_define(_env, "this", _func.get("owner"))

            # execute once
            cs_execute(_env, _once=True)
            
    # return result
    return _env.stack.pop()


"""CLASS"""
def cs_constructor(_env:CSXEnvironment, _argument_size:int):
    """ Creates a new class
        
        Parameters
        ----------
        _env : CSXEnvironment
        _argument_size : int
    """

    assert cs_is_constructor(_env.stack.top()), "not a constructor '%s'!" % _env.stack.top().type

    _class_proto = _env.stack.pop()

    _new_class = _env.vheap.cs__malloc(CSObject())
    _new_class.put(__ATTRIBUTE__PROTOTYPE__, _class_proto)

    # get qualname
    _new_class.type = _class_proto.get(__ATTRIBUTE___QUALNAME__).__str__()
    
    # copy non callable/attribute
    for _k in _class_proto.keys():
        if  not cs_is_callable(_class_proto.get(_k)):
            _new_class.put(_k, _class_proto.get(_k))

    # ============= PUSH STACK|
    # ========================|
    _env.stack.push(_new_class)

    # push method to stack
    cs_get_method(_env, __ATTRIBUTE_INITIALIZE__)

    # request call
    _func = _env.stack.pop()

    match _func.meth:

        case CSTypes.TYPE_CSNATIVEFUNCTION:
            # call function
            _args = [_env]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())

            # define "this"
            cs_define(_env, "this", _func.get("owner"))

            _env.stack.push(_func.call(_args))

            # remove this from scope
            cs_undefine(_env, "this")

        case CSTypes.TYPE_CSFUNCTION:
            # call function
            cs_call(_env, _func.get("code"))

            # define "this"
            cs_define(_env, "this", _func.get("owner"))

            # execute once
            cs_execute(_env, _once=True)

    if  cs_is_nulltype(_env.stack.top()):
        # pop return
        _env.stack.pop()
        
        # push back
        _env.stack.push(_new_class)

    else:
        # log info
        logger("class", "class constructor '%s' returned a value !!!" % _new_class.type)



def cs_new_scope(_env:CSXEnvironment):
    """ Creates new local scope

        Parameters
        ----------
        _env : CSXEnvironment
    """
    _env.calls.top().locvars.append(
        Scope(_parent=_env.calls.top().locvars[-1])
    )


def cs_end_scope(_env:CSXEnvironment):
    """ Creates new local scope

        Parameters
        ----------
        _env : CSXEnvironment
    """
    _env.calls.top().locvars.pop()


def cs_init_builtin(_env:CSXEnvironment):
    """ Initialize builtins

        Parameters
        ----------
        _env : CSXEnvironment
    """ 
    # linkage
    for each_class in ln: each_class().link([_env])



def cs_call(_env:CSXEnvironment, _csrawcode:csrawcode):
    """ Calls a user defined function

        Parameters
        ----------
        _env : CSXEnvironment
        _csrawcode : csrawcode
    """

    # check for overflow!!!!
    if  _env.calls.size() >= _env.MAX_CALL_STACK:
        raise RecursionError("StackOverflow!!!!")

    ######################################
    ## push frame
    _env.calls.push(CallFrame(_csrawcode, _env.scope[-1]))



def cs_run(_code:csrawcode):
    """ 
    """ 
    _env = CSXEnvironment()

    # initialize before run
    cs_init_builtin(_env)

    # call module
    cs_call(_env, _code)

    # run vm
    cs_execute(_env)

    # collect python
    collect()