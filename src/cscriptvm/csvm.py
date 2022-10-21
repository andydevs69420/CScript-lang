

# ======= object|
# ==============|
from object.csobject import CSObject
# ==============|


from .csOpcode import CSOpCode
from .compilable import Instruction
from .csmemory2 import CSMemory, ObjectWrapper


class ExceptionTable:

    TABLE:list[int] = []

    @staticmethod
    def et_make(_target:int):
        ExceptionTable.TABLE.append(_target)

    @staticmethod
    def et_pop():
        ExceptionTable.TABLE.pop()
    
    @staticmethod
    def et_peek():
        return ExceptionTable.TABLE[-1]
    
    @staticmethod
    def et_is_empty():
        return len(ExceptionTable.TABLE) <= 0



class EvalStack:
    """ Evaluation stack for CSCript
    """
    
    EVAL_STACK:ObjectWrapper = [
        # +-----------------+ ^
        # | ObjectWrapper N | |
        # +-----------------+ |
        #                     |
        # +-----------------+ |
        # | ObjectWrapper 0 | |
        # +-----------------+ |
    ]

    @staticmethod
    def es_push(_object:CSObject):
        return EvalStack.EVAL_STACK\
            .append(_object)
    
    @staticmethod
    def es_peek():
        return EvalStack.EVAL_STACK[-1]

    @staticmethod    
    def es_pop():
        return EvalStack.EVAL_STACK\
            .pop()
    
    @staticmethod
    def es_isEmpty():
        return len(EvalStack.EVAL_STACK) <= 0


class Frame(object):

    def __init__(self, _instructions:list[Instruction]):
        self.localmem:list[ObjectWrapper] = []
        self.returned = False
        self.ipointer = 0

        # ======== LIST OF INTRUCTIONS|
        # ============================|
        self.instructions:list[Instruction] = _instructions

    def store_local(self, _index:int, _csobject:ObjectWrapper):
        if  len(self.localmem) <= 0 or _index >= len(self.localmem):
            _csobject.increment()
            self.localmem.append(_csobject)
            return
        # set
        _csobject.increment()
        self.localmem[_index] = _csobject
    
    def getLocalAt(self, _index:int):
        return self.localmem[_index]

    def setPointer(self, _index:int):
        self.ipointer = _index

    def next(self):
        _code = self.instructions[self.ipointer]
        self.ipointer += 1
        return _code
    
    def setReturn(self, _returned:bool):
        self.returned = _returned

    def isReturned(self):
        return self.returned or self.ipointer >= len(self.instructions)
    
    def cleanup(self):
        for objwrap in self.localmem:
            objwrap.decrement()
        self.localmem.clear()
        del self


class CallStack:
    """ Call stack handles
        call event
    """
    
    CALL_STACK:list[Frame] = [
        # CALL: N
        # +---------------+
        # | instruction 0 |
        # +---------------+
        # | ...           |
        # +---------------+
        # | instruction N |
        # +---------------+

        # CALL: 0
        # +---------------+
        # | instruction 0 |
        # +---------------+
        # | ...           |
        # +---------------+
        # | instruction N |
        # +---------------+
    ]

    @staticmethod
    def cs_hasFrame():
        return len(CallStack.CALL_STACK) > 0

    @staticmethod
    def cs_push_frame(_instruction:list[Instruction]):
        CallStack.CALL_STACK\
        .append(
            Frame(_instruction)
        )
    
    @staticmethod
    def cs_peek_frame() -> Frame:
        return CallStack.CALL_STACK[-1]
    
    @staticmethod
    def cs_pop_frame()  -> Frame:
        return CallStack.CALL_STACK.pop()


#| obj0 , obj1, obj2, obj3, obj4, obj5
#|  ^            ^           ^
#|  |            |           |
#|  +--+   +-----+           |
#|     |   |                 |
#| +---+---+-----------------+
#| |   |   |
#| x   y   z


class Memory:
    """ Memory wrapper for CSMemory
    """

    VHEAP:CSMemory = CSMemory()
    NAMES:dict[int:int] = ({

    })

    @staticmethod
    def makeSlot() -> int:
        return Memory.VHEAP.CSMakeSLot()
    
    @staticmethod
    def memSet(_offset_index:int, _csobject:ObjectWrapper):
        Memory.VHEAP.decrementAt(Memory.VHEAP.NAMES[_offset_index])
        Memory.VHEAP.incrementAt(_csobject.getOffset()            )
        Memory.VHEAP.NAMES[_offset_index] = _csobject.getOffset()

    @staticmethod
    def memGet(_offset_index:int):
        return Memory.VHEAP.getObjectAt(Memory.VHEAP.NAMES[_offset_index])


class CSVirtualMachine(ExceptionTable, CallStack, Memory):
    """ Serves as virtual machine for cscript
    """

    ISRUNNING:bool = False

    @staticmethod
    def isrunning():
        return CSVirtualMachine.ISRUNNING

    @staticmethod
    def run(_instruction:list[Instruction]):
        CSVirtualMachine.ISRUNNING = True

        # push new frame
        CallStack.cs_push_frame(_instruction)

        # run
        _top:Frame = CallStack.cs_peek_frame()

        while not _top.isReturned():
            _bcode = _top.next()
            CSVirtualMachine.evaluate(_bcode)

        _top = EvalStack.es_pop()
       
        # pop
        CallStack.cs_pop_frame()\
            .cleanup()
        
        CSVirtualMachine.ISRUNNING = False
        return _top
    
    @staticmethod
    def throw_error(_csobjectwrapper:ObjectWrapper):
        if  not ExceptionTable.et_is_empty():
            # if exception table is not empty,
            # jump to whats being returned
            _target = ExceptionTable.et_peek() // 2
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
        else:
            # TODO: replace with cscript stderr
            print(_csobjectwrapper)
            return exit(1)
    
    # ==================================== OPCODE EVALUATOR|
    # =====================================================|
    @staticmethod
    def evaluate(_instruction:Instruction):
        match _instruction.opcode:
            # OK!!!
            case CSOpCode.PUSH_CONST:
                return CSVirtualMachine\
                    .push_const(_instruction)
            # OK!!!
            case CSOpCode.PUSH_NAME:
                return CSVirtualMachine\
                    .push_name(_instruction)
            
            # OK!!!
            case CSOpCode.PUSH_LOCAL:
                return CSVirtualMachine\
                    .push_local(_instruction)
            
            # OK!!!
            case CSOpCode.MAKE_ARRAY:
                return CSVirtualMachine\
                    .make_array(_instruction)

            case CSOpCode.MAKE_OBJECT:
                return CSVirtualMachine\
                    .make_object(_instruction)

            case CSOpCode.MAKE_CLASS:
                return CSVirtualMachine\
                    .make_class(_instruction)

            case CSOpCode.MAKE_MODULE:
                return CSVirtualMachine\
                    .make_module(_instruction)
            
            case CSOpCode.GET_ATTRIB:
                return CSVirtualMachine\
                    .get_attrib(_instruction)
            
            case CSOpCode.SET_ATTRIB:
                return CSVirtualMachine\
                    .set_attrib(_instruction)
            
            # OK!!!
            case CSOpCode.STORE_NAME:
                return CSVirtualMachine\
                    .store_name(_instruction)
            
            # OK!!!
            case CSOpCode.STORE_LOCAL:
                return CSVirtualMachine\
                    .store_local(_instruction)
            
            # OK!!!
            case CSOpCode.CALL:
                return CSVirtualMachine\
                    .call(_instruction)
            
            # OK!!!
            # ================ UNARY EXPR|
            # ===========================|
            case CSOpCode.UNARY_OP:
                return CSVirtualMachine\
                    .unary_op(_instruction)
            # =============== END ========


            # OK!!!
            # =============== BINARY EXPR|
            # ===========================|
            case CSOpCode.BINARY_MUL:
                return CSVirtualMachine\
                    .binary_mul(_instruction)
            case CSOpCode.BINARY_DIV:
                return CSVirtualMachine\
                    .binary_div(_instruction)
            case CSOpCode.BINARY_MOD:
                return CSVirtualMachine\
                    .binary_mod(_instruction)
            case CSOpCode.BINARY_ADD:
                return CSVirtualMachine\
                    .binary_add(_instruction)
            case CSOpCode.BINARY_SUB:
                return CSVirtualMachine\
                    .binary_sub(_instruction)
            case CSOpCode.BINARY_LSHIFT:
                return CSVirtualMachine\
                    .binary_lshift(_instruction)
            case CSOpCode.BINARY_RSHIFT:
                return CSVirtualMachine\
                    .binary_rshift(_instruction)
            case CSOpCode.BINARY_AND:
                return CSVirtualMachine\
                    .binary_and(_instruction)
            case CSOpCode.BINARY_XOR:
                return CSVirtualMachine\
                    .binary_xor(_instruction)
            case CSOpCode.BINARY_OR:
                return CSVirtualMachine\
                    .binary_or(_instruction)
            case CSOpCode.BINARY_SUBSCRIPT:
                return CSVirtualMachine\
                    .binary_subscript(_instruction)
            # =============== END ========

            # OK!!!
            # ============== COMPARE EXPR|
            # ===========================|
            case CSOpCode.COMPARE_OP:
                return CSVirtualMachine\
                    .compare_op(_instruction)
            # =============== END ========


            # OK!!!
            # ================ INPLACE OP|
            # ===========================|
            case CSOpCode.INPLACE_POW:
                return CSVirtualMachine\
                    .inplace_pow(_instruction)
            case CSOpCode.INPLACE_MUL:
                return CSVirtualMachine\
                    .inplace_mul(_instruction)
            case CSOpCode.INPLACE_DIV:
                return CSVirtualMachine\
                    .inplace_div(_instruction)
            case CSOpCode.INPLACE_MOD:
                return CSVirtualMachine\
                    .inplace_mod(_instruction)
            case CSOpCode.INPLACE_ADD:
                return CSVirtualMachine\
                    .inplace_add(_instruction)
            case CSOpCode.INPLACE_SUB:
                return CSVirtualMachine\
                    .inplace_sub(_instruction)
            case CSOpCode.INPLACE_LSHIFT:
                return CSVirtualMachine\
                    .inplace_lshift(_instruction)
            case CSOpCode.INPLACE_RSHIFT:
                return CSVirtualMachine\
                    .inplace_rshift(_instruction)
            case CSOpCode.INPLACE_AND:
                return CSVirtualMachine\
                    .inplace_and(_instruction)
            case CSOpCode.INPLACE_XOR:
                return CSVirtualMachine\
                    .inplace_xor(_instruction)
            case CSOpCode.INPLACE_OR:
                return CSVirtualMachine\
                    .inplace_or(_instruction)
            # =============== END ========


            # OK!!!
            # =================== JUMP OP|
            # ===========================|
            case CSOpCode.POP_JUMP_IF_FALSE:
                return CSVirtualMachine\
                    .pop_jump_if_false(_instruction)
            case CSOpCode.POP_JUMP_IF_TRUE:
                return CSVirtualMachine\
                    .pop_jump_if_true(_instruction)
            case CSOpCode.JUMP_IF_FALSE_OR_POP:
                return CSVirtualMachine\
                    .jump_if_false_or_pop(_instruction)
            case CSOpCode.JUMP_IF_TRUE_OR_POP:
                return CSVirtualMachine\
                    .jump_if_true_or_pop(_instruction)
            case CSOpCode.JUMP_EQUAL:
                return CSVirtualMachine\
                    .jump_equal(_instruction)
            case CSOpCode.ABSOLUTE_JUMP:
                return CSVirtualMachine\
                    .absolute_jump(_instruction)
            case CSOpCode.JUMP_TO:
                return CSVirtualMachine\
                    .jump_to(_instruction)
            # =============== END ========

            # OK!!!
            case CSOpCode.SETUP_TRY:
                return CSVirtualMachine\
                    .setup_try(_instruction)
            
            case CSOpCode.POP_TRY:
                return CSVirtualMachine\
                    .pop_try(_instruction)

            # OK!!!
            case CSOpCode.PRINT_OBJECT:
                return CSVirtualMachine\
                    .print_object(_instruction)
            
            # OK!!!
            case CSOpCode.NO_OPERATION:
                return CSVirtualMachine\
                    .no_op(_instruction)

            # OK!!!
            case CSOpCode.POP_TOP:
                return CSVirtualMachine\
                    .pop_top(_instruction)
            # OK!!!
            case CSOpCode.RETURN_OP:
                return CSVirtualMachine\
                    .return_op(_instruction)
           
        raise NotImplementedError("opcode %s is not implemented!" % _instruction.opcode.name)
    

    # ================================== BEGIN EVAL METHODS|
    # =====================================================|

    @staticmethod
    def push_const(_instruction:Instruction):
        _obj = CSVirtualMachine.VHEAP.CSMalloc(_instruction.get("obj"))
        _obj.increment()
        EvalStack.es_push(_obj)
    
    @staticmethod
    def push_name(_instruction:Instruction):
        EvalStack.es_push(Memory.memGet(_instruction.get("offset")))
    
    @staticmethod
    def push_local(_instruction:Instruction):
        EvalStack.es_push(CallStack.cs_peek_frame().getLocalAt(_instruction.get("offset")))
    
    @staticmethod
    def make_array(_instruction:Instruction):
        _size = _instruction.get("size")

        _array = CSObject.new_array()
        for idx in range(_size):

            _element = EvalStack.es_pop()
            _element.increment()

            _array.getObject().push(_element)
        
        EvalStack.es_push(_array)
    
    @staticmethod
    def make_object(_instruction:Instruction):
        _size = _instruction.get("size")

        _object = CSObject.new()

        for idx in range(_size):
            _k = EvalStack.es_pop()
            _k.decrement()

            _v = EvalStack.es_pop()
            _v.increment()
            _object.getObject().put(_k.__str__(), _v)
        
        EvalStack.es_push(_object)

    @staticmethod
    def make_class(_instruction:Instruction):
        print(_instruction)

    @staticmethod
    def make_module(_instruction:Instruction):
        EvalStack.es_push(None)
    
    @staticmethod
    def get_attrib(_instruction:Instruction):
        _top = EvalStack.es_pop()
        EvalStack.es_push(_top.getObject().getAttribute(_instruction.get("attr")))

    @staticmethod
    def set_attrib(_instruction:Instruction):
        _top = EvalStack.es_pop()
        _att = EvalStack.es_pop()
        _att.increment()
        _top.getObject().setAttribute(_instruction.get("attr"), _att)
        EvalStack.es_push(_att)
    
    @staticmethod
    def store_name(_instruction:Instruction):
        _val = EvalStack.es_peek()
        print(_val)
        Memory.memSet(_instruction.get("offset"), _val)
    
    @staticmethod
    def store_local(_instruction:Instruction):
        CSVirtualMachine.cs_peek_frame().store_local(_instruction.get("offset"), EvalStack.es_pop())
    
    @staticmethod
    def call(_instruction:Instruction):
        _top = EvalStack.es_pop()
        EvalStack.es_push(_top.getObject().call(_instruction.get("location"), _instruction.get("size")))

    
    # ================ UNARY OPERATION|
    # ================================|
    @staticmethod
    def unary_op(_instruction:Instruction):
        _opt = _instruction.get("opt")
        _rhs = EvalStack.es_pop()
        match _opt.token:
            case "~":
                return EvalStack.es_push(_rhs.bit_not(_opt))
            case "!":
                return EvalStack.es_push(_rhs.bin_not(_opt))
            case "+":
                return EvalStack.es_push(_rhs.positive(_opt))
            case "-":
                return EvalStack.es_push(_rhs.negative(_opt))
        # error operator
        raise ValueError("invalid or not implemented op \"%s\"" % _opt.token)
    # ============================= END
    

    # =============== BINARY OPERATION|
    # ================================|
    
    @staticmethod
    def binary_mul(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().mul(_instruction.get("opt"), _rhs.getObject()))
    
    @staticmethod
    def binary_div(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().div(_instruction.get("opt"), _rhs.getObject()))

    @staticmethod
    def binary_mod(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().mod(_instruction.get("opt"), _rhs.getObject()))

    @staticmethod
    def binary_add(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().add(_instruction.get("opt"), _rhs.getObject()))

    @staticmethod
    def binary_sub(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().sub(_instruction.get("opt"), _rhs.getObject()))
    
    @staticmethod
    def binary_lshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().lshift(_instruction.get("opt"), _rhs.getObject()))
    
    @staticmethod
    def binary_rshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().rshift(_instruction.get("opt"), _rhs.getObject()))
    
    @staticmethod
    def binary_and(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().bit_and(_instruction.get("opt"), _rhs.getObject()))
    
    @staticmethod
    def binary_xor(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().bit_xor(_instruction.get("opt"), _rhs.getObject()))
    
    @staticmethod
    def binary_or(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().bit_or(_instruction.get("opt"), _rhs.getObject()))
    
    @staticmethod
    def binary_subscript(_instruction:Instruction):
        _obj    = EvalStack.es_pop()
        _member = EvalStack.es_pop()
        EvalStack.es_push(_obj.getObject().subscript(_instruction.get("location"), _member.getObject()))
    # ============================= END

    
    # ===================== COMPARE OP|
    # ================================|
    @staticmethod
    def compare_op(_instruction:Instruction):
        _opt = _instruction.get("opt")
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()

        print(_lhs, _rhs)
        
        match _opt.token:
            case "<":
                return EvalStack.es_push(_lhs.getObject().lt(_opt, _rhs.getObject()))
            case "<=":
                return EvalStack.es_push(_lhs.getObject().lte(_opt, _rhs.getObject()))
            case ">":
                return EvalStack.es_push(_lhs.getObject().gt(_opt, _rhs.getObject()))
            case ">=":
                return EvalStack.es_push(_lhs.getObject().gte(_opt, _rhs.getObject()))
            case "==":
                return EvalStack.es_push(_lhs.getObject().eq(_opt, _rhs.getObject()))
            case "!=":
                return EvalStack.es_push(_lhs.getObject().neq(_opt, _rhs.getObject()))
        # error operator
        raise ValueError("invalid or not implemented op \"%s\"" % _opt.token)
    # ============================= END



    # ===================== INPLACE OP|
    # ================================|
    @staticmethod
    def inplace_pow(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().pow(_instruction.get("opt"), _rhs.getObject()))
    @staticmethod
    def inplace_mul(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().mul(_instruction.get("opt"), _rhs.getObject()))
    @staticmethod
    def inplace_div(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().div(_instruction.get("opt"), _rhs.getObject()))
    @staticmethod
    def inplace_add(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().add(_instruction.get("opt"), _rhs.getObject()))
    @staticmethod
    def inplace_sub(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().sub(_instruction.get("opt"), _rhs.getObject()))
    @staticmethod
    def inplace_lshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().lshift(_instruction.get("opt"), _rhs.getObject()))
    @staticmethod
    def inplace_rshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.getObject().rshift(_instruction.get("opt"), _rhs.getObject()))
    # ============================= END



    # ======================== JUMP OP|
    # ================================|
    # NOTE: divide target by 2 to get the exact index
    @staticmethod
    def pop_jump_if_false(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_pop()

        if not (_top.getObject().get("this")):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)

    @staticmethod
    def pop_jump_if_true(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_pop()

        if _top.getObject().get("this"):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
    
    @staticmethod
    def jump_if_false_or_pop(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_peek()

        if not _top.getObject().get("this"):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
            return

        EvalStack.es_pop()
    
    @staticmethod
    def jump_if_true_or_pop(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_peek()

        if _top.getObject().get("this"):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
            return
            
        EvalStack.es_pop()

    @staticmethod
    def jump_equal(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()

        if _lhs.getObject().equals(_rhs.getObject()):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)

    @staticmethod
    def absolute_jump(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        CallStack\
            .cs_peek_frame()\
                .setPointer(_target)

    @staticmethod
    def jump_to(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        CallStack\
            .cs_peek_frame()\
                .setPointer(_target)

    # ============================= END

    @staticmethod
    def setup_try(_instruction:Instruction):
        ExceptionTable.et_make(_instruction.get("target"))
    
    @staticmethod
    def pop_try(_instruction:Instruction):
        ExceptionTable.et_pop()

    @staticmethod
    def print_object(_instruction:Instruction):
        _size = _instruction.get("size")

        _fmt = ""
        for count in range(_size):
            _fmt += "%s" % EvalStack.es_pop().getObject().get("this")
            if  count < (_size - 1):
                _fmt += " "

        # TODO: use cscript stdout instead of python print
        print(_fmt)
    
    @staticmethod
    def no_op(_instruction:Instruction):
        pass

    @staticmethod
    def pop_top(_instruction:Instruction):
        EvalStack.es_pop()

    @staticmethod
    def return_op(_instruction:Instruction):
        CallStack.cs_peek_frame().setReturn(True)


