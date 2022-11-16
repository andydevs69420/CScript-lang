
import gc
from sys import exit
from enum import Enum
from gc import collect
from builtins import filter, print

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
from csbuiltins import CSArray
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
        self.scope = [Scope(_parent=None, _initial={})]   # global scope
        self.vheap = VHEAP(self) # virtual heap
        self.stack = STACK()     # evaluation stack
        self.calls = STACK()     # callstack
        self.error = STACK()     # errorstack
        


class STACK(object):
    """ list stack wrapper
    """

    def __init__(self):
        self.__internal = [
        ]
    
    def push(self, _any):
        self.__internal.append(_any)

    def pop(self):
        return self.__internal.pop()
    
    def top(self):
        return self.__internal[-1]
    
    def get(self, _index:int):
        return self.__internal[_index]

    def set(self, _index:int, _any:object):
        self.__internal[_index] = _any

    def all(self):
        return self.__internal
    
    def size(self):
        return len(self.__internal)


class MarkFlags(Enum):
    WHITE = 0xffffff
    GRAY  = 0x567672
    BLACK = 0x000000

class ObjectAge(Enum):
    OLD = 0x01
    NEW = 0x02


class VHEAP(object):
    """ Serves as heap memory
    """

    # NEW!!! intead of using magic number
    ALLOCATION_SIZE = 1000

    # NEW!!! intead of using magic number
    OBJECTS_LIMITER = 40_000

    def __init__(self, _env:CSXEnvironment):
        self.__bucket = []
        # unused index
        self.__unused = []
        self.__csxenv = _env

        self.__allocs = 0
        self.__trashc = 0
        self.__squeue = [] # scanqueue
        self.__gcroot = CSObject()


        self.__cyclec = 0
    
    def cs__is_alloc(self, _csobject:CSObject):
        """ Check if object is already allocated

            Parameters
            ----------
            _csobject : CSObject

            Returns
            ------
            bool
        """
        return _csobject.offset != -69420
    
    def cs__malloc(self, _csobject:CSObject):
        """ Allocates object

            Parameters
            ----------
            _csobject : CSObject

            Returns
            -------
            CSObject
        """
        if  self.cs__is_alloc(_csobject):
            # prevent double allocation
            return _csobject

        #$$$$ check first
        self.__on_allocate()

        _csobject.objage = ObjectAge.NEW

        if  len(self.__unused) > 0:
            # =========== RE-USE SLOT|
            # =======================|
            _unused = self.__unused.pop()

            # ============ SET OFFSET|
            # =======================|
            _csobject.offset = _unused

            # ======== SET AND RETURN|
            # =======================|
            self.__bucket[_unused] = _csobject
            return _csobject
        
        # ========= INSERT AND RETURN|
        # ===========================|
        _csobject.offset = len(self.__bucket)
        self.__bucket.append(_csobject)

        return _csobject
    
    def cs__object_at(self, _address_offset_index:int):
        """ Retrieves object at certain index/offset

            Parameters
            ----------
            _address_offset_index : int

            Returns
            -------
            CSObject
        """
        return self.__bucket[_address_offset_index]


    def __on_allocate(self):
        """ Frees up memory every "VHEAP.ALLOCATION_SIZE" allocation.

            If number of object inside the heap memory is 
                greaterthan or equal to "VHEAP.OBJECTS_LIMITER",
                the system will throws MemoryError
        """
        self.__allocs += 1

        if  self.__allocs >= VHEAP.ALLOCATION_SIZE:
            self.collect()
            self.__allocs = 0

            if  len(self.__unused) <= 0 and len(self.__bucket) >= VHEAP.OBJECTS_LIMITER:
                gc.collect()
                raise MemoryError("No avaiable memory!!!")

    # __________________ GC METHODS

    def gmark__phase(self):
        """ Marks reachable object
        """
        # root nodes are global variables or localvariables that are assigned to objects in heap!.
        self.__squeue.extend([
            self.__bucket[_idx] for each_scope in self.__csxenv.scope for _idx in each_scope.all_address()
        ])

        for each_node in self.__squeue:
            each_node.cstate = MarkFlags.GRAY

        while len(self.__squeue) > 0:

            _top = self.__squeue.pop()

            if  _top.cstate != MarkFlags.BLACK:
                _top.cstate  = MarkFlags.BLACK

                for each_child in _top.all():
                    # NOTE: ALL CSOjects has "all()" method, that retrieves al its reference.
                    each_child.cstate = MarkFlags.GRAY
                    self.__squeue.append(each_child)

    
    def sweep__phase(self):
        """ Delete/free, unmarked object and resets markbit for each marked objects.
        """
        for each_obj in self.__bucket:
            if  each_obj:
                if  each_obj.cstate == MarkFlags.BLACK:
                    each_obj.cstate  = MarkFlags.WHITE
                    # these objects survived, so mark them as old
                    each_obj.objage =  ObjectAge.OLD
                else:
                    match each_obj.objage:

                        case ObjectAge.OLD:
                            """ If its old and white, 
                                automatically conclude that these objects are unreachable and garbaged!!
                                (I dont't know how it's done btw!! ;D)
                            """
                            # garbage if WHITE AND OLD!!!
                            self.mark_as_garbage(each_obj)
                        
                        case ObjectAge.NEW:
                            if  self.__cyclec >= 2:
                                """ If the cycle count is greaterthan or equal to 2,
                                    and these object(s) remains "NEW" then, these object(s) is/are garbage!!
                                """
                                self.mark_as_garbage(each_obj)
        
    
    def mark_as_garbage(self, _csobject:CSObject):
        self.__bucket[_csobject.offset] = None
        self.__unused.append(_csobject.offset)
        self.__trashc += 1

    def collect(self):
        """ Collects garbage object
        """
        # print("STOPPED FOR GC COLLECTION...")
        self.gmark__phase()
        self.sweep__phase()
        self.__cyclec += 1

        if  self.__cyclec >= 5:
            """ Reset cycle count when it reaches to 5 for
                every (VHEAP.ALLOCATION_SIZE * 5)
            """
            self.__cyclec = 0

    def all(self):
        return [*filter(lambda x:x!=None, self.__bucket)]
    





class Scope(object):
    """ Acts as symbol table

        Parameters
        ----------
        _parent(optional) : Scope|None
    """

    def __init__(self, _parent, _initial):
        self.parent  = _parent
        self.symbols = ({**_initial})
    
    # for gc
    def all_address(self):
        return [_val["_address"] for _val in self.symbols.values()]

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

        # search while parent is not None
        _node = self.parent
        while _node:
            if  _node.exists(_symbol):
                return True
            _node = _node.parent
        
        return False


class StackFrame(object):
    """ Serves as StackFrame in callstack

        Parameters
        ----------
        _csrawcode : csrawcode
    """ 

    def __init__(self, _csrawcode:csrawcode, _selfscope:Scope):
        self.rawcode = _csrawcode
        self.fnscope = [_selfscope]
        self.pointer = 0
        self.locvars = STACK()
    
    def get(self, _index:int):
        return self.locvars[_index]
    
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
    if  _env.error.size() <= 0:
        return __throw__(
            _message
            + "\n"
            + _location
        )
    else:
        cs_new_string(
            _env,
            _message
            + "\n"
            + _location
        )
        # jump!!
        _env.calls.top().pointer = _env.error.top() // 2




def cs_error__NameError_define(_env:CSXEnvironment, _name:str, _loc:str):
    """ Throws name already defined error

        Parameters
        ----------
        _env  : CSXEnvironment
        _name : str
        _loc  : str
    """

    cs__error(_env, "NameError: name '%s' is already defined!!!" % _name, _loc)




def cs_error__NameError_notdef(_env:CSXEnvironment, _name:str, _loc:str):
    """ Throws name not defined error

        Parameters
        ----------
        _env  : CSXEnvironment
        _name : str
        _loc  : str
    """

    cs__error(_env, "NameError: name '%s' was not defined!!!" % _name, _loc)



def cs_error__NameError_reassign_without_define(_env:CSXEnvironment, _name:str, _loc:str):
    """ Throws re-assignment without define error

        Parameters
        ----------
        _env  : CSXEnvironment
        _name : str
        _loc  : str
    """

    cs__error(_env, "NameError: re-assigned '%s' without declairation!!!" % _name, _loc)



def cs_error__AttributeError_no_such_attribute(
    _env  : CSXEnvironment, 
    _type : CSTypes,
    _attr : str, 
    _loc  : str
):
    """ Throws error when method not found

        Parameters
        ----------
        _env  : CSXEnvironment
        _type : CSTypes
        _attr : str
        _loc  : str
    """
    cs__error(_env, "AttributeError: %s has no attribute '%s'." % (_type, _attr), _loc)



def cs_error__AttributeError_no_such_method(
    _env  : CSXEnvironment, 
    _type : CSTypes,
    _attr : str, 
    _loc  : str
):
    """ Throws error when method not found

        Parameters
        ----------
        _env  : CSXEnvironment
        _type : CSTypes
        _attr : str
        _loc  : str
    """
    cs__error(_env, "AttributeError: %s has no method '%s'." % (_type, _attr), _loc)



def cs_error__AttributeError_assignment_of_read_only(
    _env  : CSXEnvironment, 
    _type : CSTypes,
    _attr : str, 
    _loc  : str
):
    """ Throws error when method not found

        Parameters
        ----------
        _env  : CSXEnvironment
        _type : CSTypes
        _attr : str
        _loc  : str
    """
    cs__error(_env, "AttributeError: object attribute %s::%s is read-only." % (_type, _attr), _loc)





def cs_error__TypeError_not_a_constructor(_env:CSXEnvironment, _type:CSTypes, _loc:str):
    """ Throws error if not a constructor

        Parameters
        ----------
        _env  : CSXEnvironment
        _name : str
        _loc  : str
    """
    cs__error(_env, "TypeError: %s instance is not a constructor." % _type, _loc)



def cs_error__TypeError_not_subscriptible(_env:CSXEnvironment, _object_type:CSTypes, _loc:str):
    """ Throws name not defined error

        Parameters
        ----------
        _env  : CSXEnvironment
        _name : str
        _loc  : str
    """
    cs__error(_env, "TypeError: %s is not subscriptible." % _object_type, _loc)


def cs_error__TypeError_subscript_expression_type_error(
    _env : CSXEnvironment, 
    _object_type : CSTypes,
    _required : str,
    _recieved : str,
    _loc : str
):
    """ Throws type error when subscript expression missmatch

        Parameters
        ----------
        _env  : CSXEnvironment
        _name : str
        _loc  : str
    """
    cs__error(_env, "TypeError: %s subscript index/lookup must be %s, got %s." % (_object_type, _required, _recieved), _loc)


def cs_error__TypeError_invalid_r_operand(
    _env : CSXEnvironment, 
    _opt : str,
    _rhs : CSTypes, 
    _loc : str
):
    """ Throws unsupported operator for right operand

        use: unary type checking

        Parameters
        ----------
        _env : CSXEnvironment
        _opt : str
        _rhs : CSTypes
        _loc : str
    """
    cs__error(_env, "TypeError: invalid operator (%s) for right operand." % (_opt, _rhs), _loc)





def cs_error__TypeError_invalid_l_r_operand(
    _env : CSXEnvironment, 
    _lhs : CSTypes, 
    _opt : str,
    _rhs : CSTypes, 
    _loc : str
):
    """ Throws unsupported operator for both operands

        use: binary expr type checking

        Parameters
        ----------
        _env : CSXEnvironment
        _lhs : CSTypes
        _opt : str
        _rhs : CSTypes
        _loc : str
    """
    cs__error(_env, "TypeError: invalid operator (%s) for operand types(s) %s and %s." % (_opt, _lhs, _rhs), _loc)



def cs_error__TypeError_not_callable(
    _env  : CSXEnvironment, 
    _type : CSTypes, 
    _loc  : str
):
    """ Throws not callable


        Parameters
        ----------
        _env : CSXEnvironment
        _lhs : CSTypes
        _opt : str
        _rhs : CSTypes
        _loc : str
    """
    cs__error(_env, "TypeError: %s is not callable." % _type, _loc)


def cs_error__TypeError_invalid_arg_size(
    _env  : CSXEnvironment, 
    _required : int, 
    _recieved : int,
    _loc      : str
):
    """ Throws error if arg count missmatch

        Parameters
        ----------
        _env : CSXEnvironment
        _lhs : CSTypes
        _opt : str
        _rhs : CSTypes
        _loc : str
    """
    cs__error(_env, "TypeError: required argument count %d, got %d." % (_required, _recieved), _loc)


def cs_error__ZeroDivisionError(
    _env : CSXEnvironment, 
    _loc : str
):
    """ Throws zero division error

        Parameters
        ----------
        _env : CSXEnvironment
        _loc : str
    """
    cs__error(_env, "ZeroDivisionError: divisor of devidend produces zero.", _loc)

def cs_error__IndexError(_env:CSXEnvironment, _min:int, _max:int, _recieved:int, _loc:str):
    """ Throws index eror when not in range

        Parameters
        ----------
        _env : CSXEnvironment
        _min : int
        _max : int
        _recieved : int
        _loc : str
    """
    cs__error(_env, "IndexError: index %d not in range %d~%d." % (_recieved, _min, _max), _loc)


def cs_error__Throw(
    _env : CSXEnvironment, 
    _obj : CSObject,
    _loc : str
):
    """ Throws error

        Parameters
        ----------
        _env : CSXEnvironment
        _obj : CSObject
        _loc : str
    """
    _err = ...
    if  cs_has_method(_obj, "toString"):
        _env.stack.push(_obj)

        _err = cs_invoke_method(_env, _env.stack.top(), "toString", 0)
        _err = _err.__str__()

    else:
        _err = _obj.__str__()
        
    cs__error(_env, _err, _loc)




"""OPCODE INJECTION"""

def cs_dup_top(_env:CSXEnvironment):
    """ Duplicate top object

        Parameters
        ----------
        _env:CSXEnvironment
    """
    _env.stack.push(_env.stack.top())



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



def cs_evaluate(_env:CSXEnvironment, _callframe:StackFrame, _manual:bool=False):
    """
    """

    while _callframe.pointer < len(_callframe.rawcode):

        _opc:Instruction    = _callframe.rawcode.code[_callframe.pointer]
        _callframe.pointer += 1
        # print(_opc)
        
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
            
            case CSOpCode.MAKE_ARRAY:
                """"""
                cs_new_array(_env, _opc.get("size"))
            
            case CSOpCode.MAKE_OBJECT:
                """"""
                cs_new_object(_env, _opc.get("size"))

            case CSOpCode.PUSH_NAME:
                """"""
                _name = _opc.get("name")
            
                if  not cs_has_var(_env, _name):
                    cs_error__NameError_notdef(_env, _name, _opc.get("loc"))
                    continue
                
                #####
                # if  cs_has_local(_env, _name): 
                #     print("local")
                #     cs_push_local(_env, _name)
                #     # find local first!
                # else:
                #     cs_push_global(_env, _name)
                cs_push_var(_env, _name)
            

            case CSOpCode.BINARY_SUBSCRIPT:
                """"""
                if  not cs_is_subscriptible(_env.stack.top()):
                    cs_error__TypeError_not_subscriptible(_env, _env.stack.top().type, _opc.get("loc"))
                    continue

                #####
                _top_type = _env.stack.top().type


                if  cs_is_string(_env.stack.top()) or cs_is_array(_env.stack.top()):
                    _top_old = _env.stack.top()

                    # rotate 2
                    cs_rot_2(_env)

                    if  not cs_is_integer(_env.stack.top()):
                        cs_error__TypeError_subscript_expression_type_error(_env, _top_type, CSTypes.TYPE_CSINTEGER, _env.stack.top().type, _opc.get("loc"))
                        continue

                    # check range
                    if  not (_env.stack.top().this >= 0 and _env.stack.top().this < len(_top_old.this)):
                        cs_error__IndexError(_env, 0, len(_top_old.this) - 1, _env.stack.top().this, _opc.get("loc"))
                        continue

                else:
                    _top_old = _env.stack.top()

                    # rotate 2
                    cs_rot_2(_env)

                    if  not cs_is_string(_env.stack.top()):
                        cs_error__TypeError_subscript_expression_type_error(_env, _top_type, CSTypes.TYPE_CSSTRING, _env.stack.top().type, _opc.get("loc"))
                        continue
                    
                    # check attribute exist
                    if  not cs_has_attrib(_top_old, _env.stack.top().__str__()):
                        cs_error__AttributeError_no_such_attribute(_env, _top_old.type, _env.stack.top().__str__(), _opc.get("loc"))
                        continue
                
                # re-position
                cs_rot_2(_env)

                cs_subscript(_env)

                    
            case CSOpCode.SET_SUBSCRIPT:
                """"""
                if  not cs_is_subscriptible(_env.stack.top()):
                    cs_error__TypeError_not_subscriptible(_env, _env.stack.top().type, _opc.get("loc"))
                    continue


            case CSOpCode.GET_STATIC:
                """"""
                if  not cs_is_constructor(_env.stack.top()):
                    cs_error__TypeError_not_a_constructor(_env, _env.stack.top().type, _opc.get("loc"))
                    continue
                
                if  not cs_has_static(_env.stack.top(), _opc.get("attr")):
                    cs_error__AttributeError_no_such_attribute(_env, _env.stack.top().type, _opc.get("attr"), _opc.get("loc"))
                    continue
                
                #####
                cs_get_static(_env, _opc.get("attr"))
                

            case CSOpCode.SET_STATIC:
                """"""
                if  not cs_is_constructor(_env.stack.top()):
                    cs_error__TypeError_not_a_constructor(_env, _env.stack.top().type, _opc.get("loc"))
                    continue
                
                #####
                # check if attrib is read-only
                match _opc.get("attr"):
                    case SpecialAttrib.A.value|\
                         SpecialAttrib.B.value|\
                         SpecialAttrib.C.value:
                        # As for the moment, I can't freeze object!!
                        cs_error__AttributeError_assignment_of_read_only(_env, _env.stack.top().type, _opc.get("attr"), _opc.get("loc"))
                        continue

                    case _:
                        # allows making attribute
                        cs_set_static(_env, _opc.get("attr"))


            case CSOpCode.GET_ATTRIB:
                """"""
                if  not cs_has_attrib(_env.stack.top(), _opc.get("attr")):
                    cs_error__AttributeError_no_such_attribute(_env, _env.stack.top().type, _opc.get("attr"), _opc.get("loc"))
                    continue
                
                #####
                cs_get_attrib(_env, _opc.get("attr"))

            
            case CSOpCode.SET_ATTRIB:
                """"""
                if  not cs_has_attrib(_env.stack.top(), _opc.get("attr")):
                    cs_error__AttributeError_no_such_attribute(_env, _env.stack.top().type, _opc.get("attr"), _opc.get("loc"))
                    continue

                #####
                # check if attrib is read-only
                match _opc.get("attr"):
                    case SpecialAttrib.A.value|\
                         SpecialAttrib.B.value|\
                         SpecialAttrib.C.value:
                        # As for the moment, I can't freeze object!!
                        cs_error__AttributeError_assignment_of_read_only(_env, _env.stack.top().type, _opc.get("attr"), _opc.get("loc"))
                        continue

                    case _:
                        cs_set_attrib(_env, _opc.get("attr"))
            

            case CSOpCode.GET_METHOD:
                """"""
                if  not cs_has_method(_env.stack.top(), _opc.get("attr")):
                    cs_error__AttributeError_no_such_method(_env, _env.stack.top().type, _opc.get("attr"), _opc.get("loc"))
                    continue

                #####
                cs_get_method(_env, _opc.get("attr"))
            

            case CSOpCode.CALL_METHOD:
                """"""
                if  _env.stack.top().get("argc").this != _opc.get("size"):
                    cs_error__TypeError_invalid_arg_size(_env, _env.stack.top().get("argc").this, _opc.get("size"), _opc.get("loc"))
                    continue

                #####
                cs_method_call(_env, _opc.get("size"))
                return

            case CSOpCode.CALL:
                """"""
                if  not cs_is_callable(_env.stack.top()):
                    cs_error__TypeError_not_callable(_env, _env.stack.top().type, _opc.get("loc"))
                    continue

                if  _env.stack.top().get("argc").this != _opc.get("size"):
                    cs_error__TypeError_invalid_arg_size(_env, _env.stack.top().get("argc").this, _opc.get("size"), _opc.get("loc"))
                    continue

                #####
                cs_function_call(_env, _opc.get("size"))
                return
            

            case CSOpCode.POSTFIX_OP:
                raise NotImplementedError("Not implemented op '%s' !!!" % _opc.get("opt"))


            case CSOpCode.UNARY_OP:

                match _opc.get("opt"):

                    case "new":
                        """"""
                        if  not cs_is_constructor(_env.stack.top()):
                            cs_error__TypeError_not_a_constructor(_env, _env.stack.top().type, _opc.get("loc"))
                            continue
                        
                        _copy = _env.stack.top()

                        # check arg
                        cs_get_attrib(_env, __ATTRIBUTE_INITIALIZE__)
                        
                        if  _env.stack.top().get("argc").this != _opc.get("size"):
                            cs_error__TypeError_invalid_arg_size(_env, _env.stack.top().get("argc").this, _opc.get("size"))
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
                            cs_error__TypeError_invalid_r_operand(_env, _opc.get("opt"), _rhs.type, _opc.get("loc"))
                            continue

                        #####
                        cs_new_number(_env, ~ _rhs.this)
                    

                    case "+":
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_rhs):
                            cs_error__TypeError_invalid_r_operand(_env, _opc.get("opt"), _rhs.type, _opc.get("loc"))
                            continue

                        #####
                        cs_new_number(_env, + _rhs.this)
                    

                    case "-":
                        _rhs = _env.stack.pop()

                        if  not cs_is_number(_rhs):
                            cs_error__TypeError_invalid_r_operand(_env, _opc.get("opt"), _rhs.type, _opc.get("loc"))
                            continue

                        #####
                        cs_new_number(_env, - _rhs.this)
                    
                    case _:
                        raise NotImplementedError("Not implemented op '%s' !!!" % _opc.get("opt"))


            case CSOpCode.BINARY_POW:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue

                #####
                cs_new_number(_env, _lhs.this ** _rhs.this)
            

            case CSOpCode.BINARY_MUL:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue

                #####
                cs_new_number(_env, _lhs.this * _rhs.this)
            

            case CSOpCode.BINARY_DIV:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue

                # zero divisor
                if  _rhs.this == 0:
                    cs_error__ZeroDivisionError(_env, _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this / _rhs.this)
            

            case CSOpCode.BINARY_MOD:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue

                # zero divisor
                if  _rhs.this == 0:
                    cs_error__ZeroDivisionError(_env, _opc.get("loc"))
                    continue

                #####
                cs_new_number(_env, _lhs.this % _rhs.this)


            case CSOpCode.BINARY_ADD:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()
            
                if  not ((cs_is_number(_lhs) and cs_is_number(_rhs)) or \
                         (cs_is_string(_lhs) and cs_is_string(_rhs))):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type, _opc.get("loc"))
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
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue

                #####
                cs_new_number(_env, _lhs.this - _rhs.this)
            
            case CSOpCode.BINARY_LSHIFT:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_integer(_lhs) and cs_is_integer(_rhs):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue

                #####
                cs_new_number(_env, _lhs.this << _rhs.this)
            

            case CSOpCode.BINARY_RSHIFT:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not cs_is_integer(_lhs) and cs_is_integer(_rhs):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue

                #####
                cs_new_number(_env, _lhs.this >> _rhs.this)
            
            case CSOpCode.COMPARE_OP:
                match _opc.get("opt"):

                    case "<":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                            cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                            continue

                        #####
                        cs_new_boolean(_env, _lhs.this < _rhs.this)
                    
                    case "<=":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                            cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                            continue

                        #####
                        cs_new_boolean(_env, _lhs.this <= _rhs.this)
                    

                    case ">":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                            cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                            continue

                        #####
                        cs_new_boolean(_env, _lhs.this > _rhs.this)
                    
                    case ">=":
                        _lhs = _env.stack.pop()
                        _rhs = _env.stack.pop()

                        if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                            cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
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
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this & _rhs.this)
            

            case CSOpCode.BINARY_XOR:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this ^ _rhs.this)
            

            case CSOpCode.BINARY_OR:
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
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
                    cs_error__NameError_define(_env, _opc.get("name"), _opc.get("loc"))
                    continue

                #####
                cs_make_var(_env, _opc.get("name"))
            
            case CSOpCode.MAKE_LOCAL:
                """"""
                if  cs_has_local(_env, _opc.get("name")):
                    cs_error__NameError_define(_env, _opc.get("name"), _opc.get("loc"))
                    continue

                #####
                cs_make_local(_env, _opc.get("name"))
            
            case CSOpCode.MAKE_PARAM:
                """"""
                if  cs_has_local(_env, _opc.get("name")):
                    cs_error__NameError_define(_env, _opc.get("name"), _opc.get("loc"))
                    continue

                #####
                cs_make_param(_env, _opc.get("name"), _opc.get("offset"))
            
            case CSOpCode.STORE_NAME:
                """"""
                _name = _opc.get("name")

                if  not cs_has_var(_env, _name):
                    cs_error__NameError_reassign_without_define(_env, _name, _opc.get("loc"))
                    continue

                #####
                # if  cs_has_local(_env, _name): cs_store_local(_env, _name)
                #     # find local first!
                # else:
                #     cs_store_name(_env, _name)
                cs_store_var(_env, _name)
                    
            
            case CSOpCode.INPLACE_POW:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this ** _rhs.this)
                
            
            case CSOpCode.INPLACE_MUL:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this * _rhs.this)
            
            case CSOpCode.INPLACE_DIV:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                # zero divisor
                if  _rhs.this == 0:
                    cs_error__ZeroDivisionError(_env, _opc.get("loc"))
                    continue
                
                #####
                cs_new_number(_env, _lhs.this / _rhs.this)
            
            case CSOpCode.INPLACE_MOD:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_number(_lhs) and cs_is_number(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                # zero divisor
                if  _rhs.this == 0:
                    cs_error__ZeroDivisionError(_env, _opc.get("loc"))
                    continue
                
                #####
                cs_new_number(_env, _lhs.this % _rhs.this)

            case CSOpCode.INPLACE_ADD:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not ((cs_is_number(_lhs) and cs_is_number(_rhs)) or \
                         (cs_is_string(_lhs) and cs_is_string(_rhs))):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
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
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this - _rhs.this)
            
            case CSOpCode.INPLACE_LSHIFT:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this << _rhs.this)
            
            case CSOpCode.INPLACE_RSHIFT:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this >> _rhs.this)
            
            case CSOpCode.INPLACE_AND:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this & _rhs.this)
            
            case CSOpCode.INPLACE_XOR:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this ^ _rhs.this)
            
            case CSOpCode.INPLACE_OR:
                """"""
                _lhs = _env.stack.pop()
                _rhs = _env.stack.pop()

                if  not (cs_is_integer(_lhs) and cs_is_integer(_rhs)):
                    cs_error__TypeError_invalid_l_r_operand(_env, _lhs.type, _opc.get("opt"), _rhs.type)
                    continue
                
                #####
                cs_new_number(_env, _lhs.this | _rhs.this)
            

            case CSOpCode.POP_JUMP_IF_FALSE:
                """"""
                _top = _env.stack.pop()

                if  cs_is_nulltype(_top) or cs_is_bool_false(_top):
                    _callframe.pointer = _opc.get("target") // 2
            
            case CSOpCode.POP_JUMP_IF_TRUE:
                """"""
                _top = _env.stack.pop()

                if  not (cs_is_nulltype(_top) or cs_is_bool_false(_top)):
                    _callframe.pointer = _opc.get("target") // 2
            

            case CSOpCode.JUMP_IF_TRUE_OR_POP:
                """"""
                _top = _env.stack.top()

                if  (not cs_is_nulltype(_top)) or cs_is_bool_true(_top):
                    _callframe.pointer = _opc.get("target") // 2
                    continue
                
                ##### pop
                _env.stack.pop()


            case CSOpCode.JUMP_IF_FALSE_OR_POP:
                """"""
                _top = _env.stack.top()

                if  cs_is_nulltype(_top) or cs_is_bool_false(_top):
                    _callframe.pointer = _opc.get("target") // 2
                    continue
                
                ##### pop
                _env.stack.pop()

            case CSOpCode.JUMP_EQUAL:
                """"""
                _a = _env.stack.pop()
                _b = _env.stack.pop()

                if  not (cs_is_pointer(_a) or cs_is_pointer(_b)):
                    if  _a.this == _b.this:
                        _callframe.pointer = _opc.get("target") // 2
                else:
                    if  _a.offset == _b.offset:
                        _callframe.pointer = _opc.get("target") // 2

            case CSOpCode.ABSOLUTE_JUMP:
                """"""
                _callframe.pointer = _opc.get("target") // 2
            

            case CSOpCode.JUMP_TO:
                """"""
                _callframe.pointer = _opc.get("target") // 2
            

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

                    if  cs_has_method(_top, "toString") and not cs_is_string(_top):
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
                cs_error__Throw(_env, _env.stack.pop(), _opc.get("loc"))
            
            case CSOpCode.SETUP_TRY:
                """"""
                _env.error.push(_opc.get("target"))
            
            case CSOpCode.POP_TRY:
                """"""
                _env.error.pop()
            
            case CSOpCode.NO_OPERATION:
                """"""
                pass

            case CSOpCode.RETURN_OP:
                """"""
                _env.calls.pop()
                return

            case _:
                print("Not implemented opcode", _opc.opcode.name)
                exit(1)


"""NAME HELPERS"""

def cs_ifdef(_env:CSXEnvironment, _name:str):
    """ Checks if name exists to local scope

        same as cs_has_local. Just for classification

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    return _env.scope[-1].exists(_name, _local=True)


def cs_has_var(_env:CSXEnvironment, _name:str):
    """ Checks if name exists in local->global scope

        Allow cascade search

        Parameters
        ----------
        _env  : CSXEnvironment
        _name : str

        Returns
        -------
        bool
    """
    return _env.calls.top().fnscope[-1].exists(_name, _local=False)


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
    if  not _env.calls.top().fnscope[-1].exists(_name, _local=False):
        return False

    # retrieve
    _info = _env.calls.top().fnscope[-1].lookup(_name)

    return _info["_global"]

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
    if  not _env.calls.top().fnscope[-1].exists(_name, _local=True):
        return False

    # retrieve
    _info = _env.calls.top().fnscope[-1].lookup(_name)

    return (not _info["_global"])

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

    # retrieve
    _infor = _env.scope[-1].lookup(_class_name)
   
    _class = _env.vheap.cs__object_at(_infor["_address"])
    
    # check if valid class
    return cs_is_constructor(_class)




"""MEMBER HELPERS"""


    

def cs_has_static(_obj:CSObject, _static_attr:str):
    """ Checks if class proto has static attribute "_static_attr:str"

        Parameters
        ----------
        _obj : CSObject
        _static_attr : str

        Returns
        -------
        bool
    """
    assert cs_is_constructor(_obj), "Not a constructor!!"
    return _obj.hasKey(_static_attr)



def cs_has_attrib(_obj:CSObject, _attrib:str):
    """ Checks objecto has attribute "_attrib:str"

        Parameters
        ----------
        _obj : CSObject
        _attrib : str

        Returns
        -------
        bool
    """
    return _obj.hasKey(_attrib)



"""OBJECT HELPERS"""

def cs_verify(_env:CSXEnvironment, _csobject:CSObject):
    assert _csobject == _env.vheap.cs__object_at(_csobject.offset), "invalid object signiture!!!!"

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


def cs_has_method(_obj:CSObject, _method_name:str):
    """ Checks if _obj has _method_name to its class proto

        Parameters
        ----------
        _obj : CSObject
        _method_name : str

        Returns
        -------
        bool
    """
    # if contains "__proto__"
    if  not cs_has_attrib(_obj, __ATTRIBUTE__PROTOTYPE__): 
        return False

    # search in class
    _class = _obj.get(__ATTRIBUTE__PROTOTYPE__)

    if  not cs_has_attrib(_class, _method_name):
        return False

    return cs_is_callable(_class.get(_method_name))


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


def cs_is_array(_csobject:CSObject):
    """ Checks if object is an array

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSARRAY


def cs_is_hashmap(_csobject:CSObject):
    """ Checks if object is hashmap

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSHASHMAP


def cs_is_callable(_obj:CSObject|CSFunction|CSNativeFunction):
    """ Checks if object is a function

        Parameters
        ----------
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

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSNATIVEFUNCTION


def cs_is_function(_csobject:CSObject):
    """ Checks if object is a user function

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSFUNCTION


def cs_is_method(_csobject:CSObject):
    """ Checks if object is a method

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return _csobject.type == CSTypes.TYPE_CSMETHOD


def cs_is_subscriptible( _obj:CSObject):
    """ Checks if an object can be subscript

        Parameters
        ----------
        _csobject : CSObject

        Returns
        -------
        bool
    """
    return (cs_is_pointer(_obj) or cs_is_string(_obj)) and not cs_is_callable(_obj)


"""NAME CREATION | SETTING | RETRIEVAL"""

def cs_define(_env:CSXEnvironment, _name:str, _value:CSObject):
    """ Creates local variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
        _value : CSObject
    """
    assert not cs_ifdef(_env, _name), "Name '%s' already defined!" % _name

    # save var
    _env.scope[-1].insert(_name, _address=_value.offset, _global=False)


def cs_undefine(_env:CSXEnvironment, _name:str):
    """ Removes local variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert cs_ifdef(_env, _name), "name '%s' is not defined!" % _name

    # save var
    _env.scope[-1].delete(_name)


def cs_assert_dirty(_env:CSXEnvironment, _csobject:CSObject):
    """ Checks if valid object

        Parameters
        ----------
        _env : CSXEnvironment
        _csobject : CSObject

        Return
        ----------
        _csobject  
    """
    if  _csobject.offset < 0:
        return
    if  _csobject != _env.vheap.cs__object_at(_csobject.offset):
        print("Invalid object signiture", _csobject, "!!!")
        exit(1)

def cs_make_var(_env:CSXEnvironment, _name:str):
    """ Creates global variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert not cs_has_global(_env, _name), "name '%s' already defined!" % _name

    # try allocate
    _value = _env.stack.pop()

    cs_assert_dirty(_env, _value)

    # check if primitive
    if  not cs_is_pointer(_value):
        """ If not pointer type
            convert it to pointer, as its ready of it.
        """
        _value = _env.vheap.cs__malloc(_value)

    # save var
    _env.scope[-1].insert(_name, _address=_value.offset, _global=True)


def cs_make_local(_env:CSXEnvironment, _name:str):
    """ Creates local variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert not cs_has_local(_env, _name), "name '%s' already defined!" % _name

    # if local, address is the top stack index
    # of its localstack
    _address = _env.calls.top().locvars.size()

    cs_assert_dirty(_env, _env.stack.top())

    # save var
    _env.calls.top().fnscope[-1].insert(_name, _address=_address, _global=False)
  
    # pop from eval stack
    _env.calls.top().locvars.push(_env.stack.pop())


def cs_make_param(_env:CSXEnvironment, _name:str, _offset:int):
    """ Creates parameter variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert not cs_has_local(_env, _name), "name '%s' already defined!" % _name

    # if local, address is the top stack index
    _address = ((_env.stack.size() - 1) - _offset)

    # save var
    _env.scope[-1].insert(_name, _address=_address, _global=False)

def cs_store_var(_env:CSXEnvironment, _name:str):
    """ Reassign local/global variable
        
        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert cs_has_var(_env, _name), "no such name '%s'" % _name

    # try alloc


    # update value
    if  cs_has_global(_env, _name):
        _value = _env.stack.pop()

        if  not cs_is_pointer(_value):
            """ If not pointer type
                convert it to pointer, as its ready of it.
            """
            _value = _env.vheap.cs__malloc(_value)
        _env.scope[-1].update(_name, _address=_value.offset)

    else:
        _address = _env.calls.top().locvars.size()

        cs_assert_dirty(_env, _env.stack.top())

        # save var
        _env.calls.top().fnscope[-1].update(_name, _address=_address)
    
        # pop from eval stack
        _env.calls.top().locvars.push(_env.stack.pop())

def cs_push_var(_env:CSXEnvironment, _name:str):
    """ Gets global/local variable value

        Parameters
        ----------
        _env : CSXEnvironment
        _name : str
    """
    assert cs_has_var(_env, _name), "No such name '%s'" % _name

    # retrieve starts from local to global
    _info = _env.calls.top().fnscope[-1].lookup(_name)
    _addr = _info["_address"]

    # push to stack
    if  cs_has_global(_env, _name):
        _env.stack.push(_env.vheap.cs__object_at(_addr))
    else:
        _env.stack.push(_env.calls.top().locvars.get(_addr))


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


"""OBJECT CREATION"""

def cs_new_code(_env:CSXEnvironment, _raw_code:csrawcode):
    """ Push number to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _raw_code : csrawcode
    """ 
    _env.stack.push(_raw_code)


def cs_new_number(_env:CSXEnvironment, _py_number:int|float):
    """ Push number to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_number : int|float
    """ 
    if  type(_py_number) == int:
        # push #
        _env.stack.push(CSInteger(_py_number))
    else:
        # push #
        _env.stack.push(CSDouble(_py_number))



def cs_new_string(_env:CSXEnvironment, _py_string:str):
    """ Push string to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_string : str
    """ 
    # push #
    _env.stack.push(CSString(_py_string))


def cs_new_boolean(_env:CSXEnvironment, _py_boolean:bool):
    """ Push boolean to stack

        Parameters
        ----------
        _env : CSXEnvironment
        _py_boolean : bool
    """ 
    # push #
    _env.stack.push(CSBoolean(_py_boolean))



def cs_new_nulltype(_env:CSXEnvironment):
    """ Push boolean to stack

        Parameters
        ----------
        _env : CSXEnvironment
    """
    # push #
    _env.stack.push(CSNullType())


def cs_new_array(_env:CSXEnvironment, _pop_size:int):
    """ Push array to stack

        # NOTE: Pointer type!!!

        Parameters
        ----------
        _env : CSXEnvironment
        _pop_size : int
    """ 
    _obj = _env.vheap.cs__malloc(CSArray())

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())

    for _r in range(_pop_size):
        _elm = _env.stack.pop()

        # finally push
        _obj.local_push(_elm)
    
    # push #
    _env.stack.push(_obj)


def cs_new_object(_env:CSXEnvironment, _pop_size:int):
    """ Push hahsmap to stack

        # NOTE: Pointer type!!!

        Parameters
        ----------
        _env : CSXEnvironment
        _pop_size : int
    """
    _obj = _env.vheap.cs__malloc(CSHashMap())

    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())
    

    for _r in range(_pop_size):
        _key = _env.stack.pop()
        _val = _env.stack.pop()

        # set marked bit first
        _val.marked = True

        # finally put
        _obj.put(_key.__str__(), _val)

    # push #
    _env.stack.push(_obj)


def cs_new_class(_env:CSXEnvironment, _pop_size:int):
    """ Push/Builds a class prototype

        Parameters
        ----------
        _env : CSXEnvironment
        _pop_size : int
    """
    _class_proto_name = _env.stack.pop()

    # creates new object as class proto
    _obj =_env.vheap.cs__malloc(CSObject())

    # set qualifed name
    _obj.put(__ATTRIBUTE___QUALNAME__, _class_proto_name)

    for _r in range(_pop_size):
        _key = _env.stack.pop()
        _val = _env.stack.pop()
        _obj.put(_key.__str__(), _val)
    
    # push #
    _env.stack.push(_obj)


def cs_new_function(_env:CSXEnvironment):
    """ Push/Builds a function

        # NOTE: Pointer type!!!

        Parameters
        ----------
        _env : CSXEnvironment
    """
    _fname = _env.stack.pop()
    _fargc = _env.stack.pop()
    _fcode = _env.stack.pop()

    _obj = _env.vheap.cs__malloc(CSFunction(_fname, _fargc, _fcode))
    
    if  cs_has_class(_env, _obj.type): #$
        # push to top
        cs_get_class(_env, _obj.type)

        # pop and put
        _obj.put(__ATTRIBUTE__PROTOTYPE__, _env.stack.pop())

    # allocate before push
    _env.stack.push(_obj)


def cs_constructor(_env:CSXEnvironment, _argument_size:int):
    """ Creates a new instance
        
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

            _env.stack.push(_func.call(_args))

        case CSTypes.TYPE_CSFUNCTION:
            # call function

            # wrap code to StackFrame
            _env.calls.push( # include its local scope
                StackFrame(_func.get("code"), Scope(_parent=_env.calls.top().fnscope[-1], _initial={
                    # make "this" reference as a local variable!!
                    # instead parsing "this" keyword and popping from stack.
                    "this": {"_address": 0, "_global": False}
                })))

            _env.calls.top().locvars.push(_func.get("this"))
           
            # cs_evaluate should return None after call
            cs_evaluate(_env, _env.calls.top(), True)

    
    if  cs_is_nulltype(_env.stack.top()):
        # pop return
        _env.stack.pop()
       
        # push back
        _env.stack.push(_new_class)
        
    else:
        # log info
        logger("class", "class constructor '%s' returned a value !!!" % _new_class.type)


"""MEMBER"""

def cs_subscript(_env:CSXEnvironment):
    """ Pushes member of an object to stack

        Parameters
        ----------
        _env : CSXEnvironment
    """
    assert cs_is_subscriptible(_env.stack.top()), "Not subcriptible!!!"

    _obj = _env.stack.pop()
    _exp = _env.stack.pop()

    match _obj.type:
        case CSTypes.TYPE_CSSTRING:
            cs_new_string(_env, _obj.this[_exp.this])

        case CSTypes.TYPE_CSARRAY:
            _env.stack.push(_obj.this[_exp.this])

        case _:
            _env.stack.push(_obj.get(_exp.__str__()))


def cs_get_static(_env:CSXEnvironment, _attr:str):
    """ Push static attribute of Class proto to stack

        Parameters
        ----------
        _env  : CSXEnvironment
        _attr : str
    """
    assert cs_is_constructor(_env.stack.top()), "Not a constructor!!!"
    _env.stack.push(_env.stack.pop().get(_attr))



def cs_set_static(_env:CSXEnvironment, _attr:str):
    """ Make/update static attribute on Class proto

        Parameters
        ----------
        _env  : CSXEnvironment
        _attr : str
    """
    assert cs_is_constructor(_env.stack.top()), "Not a constructor!!!"
    _env.stack.pop().put(_attr, _env.stack.pop())



def cs_get_attrib(_env:CSXEnvironment, _attr:str):
    """ Push  attribute of object to stack

        Parameters
        ----------
        _env  : CSXEnvironment
        _attr : str
    """
    assert cs_has_attrib(_env.stack.top(), _attr), "Not a constructor!!!"
    _env.stack.push(_env.stack.pop().get(_attr))



def cs_set_attrib(_env:CSXEnvironment, _attr:str):
    """ Set attribute of an object

        Parameters
        ----------
        _env  : CSXEnvironment
        _attr : str
    """
    assert cs_has_attrib(_env.stack.top(), _attr), "Not a constructor!!!"
    _env.stack.pop().put(_attr, _env.stack.pop())



def cs_get_method(_env:CSXEnvironment, _method_name:str):
    """ Extracts method from class prototype

        Parameters
        ----------
        _env : CSXEnvironment
        _method_name : str
        
    """
    assert cs_has_method(_env.stack.top(), _method_name), "No such method '%s'" % _method_name

    # top object
    _objct = _env.stack.pop()
    
    # class becomes __proto__
    _class = _objct.get(__ATTRIBUTE__PROTOTYPE__)

    # push to stack
    _env.stack.push(_env.vheap.cs__malloc(CSMethod(_objct, _class.get(_method_name))))


"""FUNCTIONS"""

def cs_method_call(_env:CSXEnvironment, _argument_size:int):
    """ Calls a method

        Parameters
        ----------
        _env : CSXEnvironment
        _argument_size : int
    """
    assert cs_is_callable(_env.stack.top()), "Not a function!"
    
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
            _args = [
                _env, 
                # make "this" as a second argument,
                # if a method is native from python.
                _func.get("this") # thisArg
            ]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())

            # add native scope
            cs_new_scope(_env)

            _env.stack.push(_func.call(_args))

            # pop native scope
            cs_end_scope(_env)


        case CSTypes.TYPE_CSFUNCTION:
            # call function

            # wrap code to StackFrame
            _env.calls.push( # include its local scope
                StackFrame(_func.get("code"), Scope(_parent=_env.calls.top().fnscope[-1], _initial={
                    # make "this" reference as a local variable!!
                    # instead parsing "this" keyword and popping from stack.
                    "this": {"_address": 0, "_global": False}
                })))

            _env.calls.top().locvars.push(_func.get("this"))
           
            # cs_evaluate should return None after call


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
            _args = [
                _env, 
                # make "this" as a second argument,
                # if a method is native from python.
                _func.get("this") # thisArg
            ]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())
            
            # add native scope
            cs_new_scope(_env)

            _env.stack.push(_func.call(_args))

            # pop native scope
            cs_end_scope(_env)

        case CSTypes.TYPE_CSFUNCTION:
            # call function

            # wrap code to StackFrame
            _env.calls.push( # include its local scope
                StackFrame(_func.get("code"), Scope(_parent=_env.calls.top().fnscope[-1], _initial={})))
           
            # cs_evaluate should return None after call


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
    assert cs_has_method(_obj, _method_name), "No such method '%s'" % _method_name

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
            _args = [
                _env, 
                # make "this" as a second argument,
                # if a method is native from python.
                _func.get("this") # thisArg
            ]

            for _r in range(_argument_size):
                _args.append(_env.stack.pop())

            # add native scope
            cs_new_scope(_env)

            _env.stack.push(_func.call(_args))

            # pop native scope
            cs_end_scope(_env)

        case CSTypes.TYPE_CSFUNCTION:
            # call function


            # wrap code to StackFrame
            _env.calls.push( # include its local scope
                StackFrame(_func.get("code"), Scope(_parent=_env.calls.top().fnscope[-1], _initial={
                    # make "this" reference as a local variable!!
                    # instead parsing "this" keyword and popping from stack.
                    "this": {"_address": 0, "_global": False}
                })))

            _env.calls.top().locvars.push(_func.get("this"))

           
            # cs_evaluate should return None after call
            cs_evaluate(_env, _env.calls.top(), True)

            
    # return result
    return _env.stack.pop()


"""SCOPE CREATION | DELETION"""

def cs_new_scope(_env:CSXEnvironment):
    """ Creates new local scope

        Parameters
        ----------
        _env : CSXEnvironment
    """

    _env.calls.top().fnscope.append(
        Scope(_parent=_env.calls.top().fnscope[-1], _initial={"yawa":2})
    )


def cs_end_scope(_env:CSXEnvironment):
    """ Creates new local scope

        Parameters
        ----------
        _env : CSXEnvironment
    """
    _env.calls.top().fnscope.pop()




"""VM SETUP"""

def cs_init_builtin(_env:CSXEnvironment):
    """ Initialize builtins

        Parameters
        ----------
        _env : CSXEnvironment
    """ 

    # linkage
    # for each_class in ln: each_class().link([_env])


def cs_user_call(_env:CSXEnvironment, _csrawcode:csrawcode):
    """
    """
    # check for overflow!!!!
    if  _env.calls.size() >= _env.MAX_CALL_STACK:
        raise RecursionError("StackOverflow!!!!")


    


def cs_run(_code:csrawcode):
    """ 
    """ 
    _env = CSXEnvironment()

    # initialize before run
    cs_init_builtin(_env)

    # wrap code to StackFrame
    _env.calls.push( # include its local scope
        StackFrame(_code, Scope(_parent=_env.scope[-1], _initial={})))
    
    _env.calls.top().fnscope = _env.scope
    
    while (_env.calls.size() > 0):
        cs_evaluate(_env, _env.calls.top())

    # collect python
    collect()