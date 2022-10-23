from astnode.utils.compilable import Instruction

# ======= object|
# ==============|
from object.csobject import CSObject
# ==============|


from .csOpcode import CSOpCode
from .csmemory3 import CSMemoryObject
from .csframe import Frame


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
    
    EVAL_STACK:CSObject = [
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



class CSVM(ExceptionTable, CallStack):
    """ Serves as virtual machine for cscript
    """
    VHEAP:CSMemoryObject = CSMemoryObject()

    ISRUNNING:bool = False

    @staticmethod
    def isrunning():
        return CSVM.ISRUNNING

    @staticmethod
    def run(_instruction:list[Instruction]):
        CSVM.ISRUNNING = True

        # push new frame
        CallStack.cs_push_frame(_instruction)

        # run
        _top:Frame = CallStack.cs_peek_frame()

        while not _top.isReturned():
            _bcode = _top.next()
            CSVM.evaluate(_bcode)

        _top = EvalStack.es_pop()
       
        # pop
        CallStack.cs_pop_frame()\
            .cleanup()
        
        CSVM.ISRUNNING = False
        return _top
    
    @staticmethod
    def throw_error(_csobject:CSObject):
        if  not ExceptionTable.et_is_empty():
            print("Called IF")
            # if exception table is not empty,
            # jump to whats being returned
            _target = ExceptionTable.et_peek() // 2
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
        else:
            # TODO: replace with cscript stderr
            print(_csobject)
            return exit(1)
    
    # ==================================== OPCODE EVALUATOR|
    # =====================================================|
    @staticmethod
    def evaluate(_instruction:Instruction):
        match _instruction.opcode:
            # OK!!!
            case CSOpCode.PUSH_CONST:
                return CSVM\
                    .push_const(_instruction)
            # OK!!!
            case CSOpCode.PUSH_NAME:
                return CSVM\
                    .push_name(_instruction)
            
            # OK!!!
            case CSOpCode.PUSH_LOCAL:
                return CSVM\
                    .push_local(_instruction)
            
            # OK!!!
            case CSOpCode.MAKE_ARRAY:
                return CSVM\
                    .make_array(_instruction)

            case CSOpCode.MAKE_OBJECT:
                return CSVM\
                    .make_object(_instruction)

            case CSOpCode.MAKE_CLASS:
                return CSVM\
                    .make_class(_instruction)

            case CSOpCode.MAKE_MODULE:
                return CSVM\
                    .make_module(_instruction)
            
            case CSOpCode.GET_ATTRIB:
                return CSVM\
                    .get_attrib(_instruction)
            
            case CSOpCode.SET_ATTRIB:
                return CSVM\
                    .set_attrib(_instruction)
            
            # OK!!!
            case CSOpCode.STORE_NAME:
                return CSVM\
                    .store_name(_instruction)
            
            # OK!!!
            case CSOpCode.STORE_LOCAL:
                return CSVM\
                    .store_local(_instruction)
            
            # OK!!!
            case CSOpCode.CALL:
                return CSVM\
                    .call(_instruction)
            
            # OK!!!
            # ================ UNARY EXPR|
            # ===========================|
            case CSOpCode.UNARY_OP:
                return CSVM\
                    .unary_op(_instruction)
            # =============== END ========


            # OK!!!
            # =============== BINARY EXPR|
            # ===========================|
            case CSOpCode.BINARY_MUL:
                return CSVM\
                    .binary_mul(_instruction)
            case CSOpCode.BINARY_DIV:
                return CSVM\
                    .binary_div(_instruction)
            case CSOpCode.BINARY_MOD:
                return CSVM\
                    .binary_mod(_instruction)
            case CSOpCode.BINARY_ADD:
                return CSVM\
                    .binary_add(_instruction)
            case CSOpCode.BINARY_SUB:
                return CSVM\
                    .binary_sub(_instruction)
            case CSOpCode.BINARY_LSHIFT:
                return CSVM\
                    .binary_lshift(_instruction)
            case CSOpCode.BINARY_RSHIFT:
                return CSVM\
                    .binary_rshift(_instruction)
            case CSOpCode.BINARY_AND:
                return CSVM\
                    .binary_and(_instruction)
            case CSOpCode.BINARY_XOR:
                return CSVM\
                    .binary_xor(_instruction)
            case CSOpCode.BINARY_OR:
                return CSVM\
                    .binary_or(_instruction)
            case CSOpCode.BINARY_SUBSCRIPT:
                return CSVM\
                    .binary_subscript(_instruction)
            # =============== END ========

            case CSOpCode.SET_SUBSCRIPT:
                return CSVM\
                    .set_subscript(_instruction)

            # OK!!!
            # ============== COMPARE EXPR|
            # ===========================|
            case CSOpCode.COMPARE_OP:
                return CSVM\
                    .compare_op(_instruction)
            # =============== END ========


            # OK!!!
            # ================ INPLACE OP|
            # ===========================|
            case CSOpCode.INPLACE_POW:
                return CSVM\
                    .inplace_pow(_instruction)
            case CSOpCode.INPLACE_MUL:
                return CSVM\
                    .inplace_mul(_instruction)
            case CSOpCode.INPLACE_DIV:
                return CSVM\
                    .inplace_div(_instruction)
            case CSOpCode.INPLACE_MOD:
                return CSVM\
                    .inplace_mod(_instruction)
            case CSOpCode.INPLACE_ADD:
                return CSVM\
                    .inplace_add(_instruction)
            case CSOpCode.INPLACE_SUB:
                return CSVM\
                    .inplace_sub(_instruction)
            case CSOpCode.INPLACE_LSHIFT:
                return CSVM\
                    .inplace_lshift(_instruction)
            case CSOpCode.INPLACE_RSHIFT:
                return CSVM\
                    .inplace_rshift(_instruction)
            case CSOpCode.INPLACE_AND:
                return CSVM\
                    .inplace_and(_instruction)
            case CSOpCode.INPLACE_XOR:
                return CSVM\
                    .inplace_xor(_instruction)
            case CSOpCode.INPLACE_OR:
                return CSVM\
                    .inplace_or(_instruction)
            # =============== END ========


            # OK!!!
            # =================== JUMP OP|
            # ===========================|
            case CSOpCode.POP_JUMP_IF_FALSE:
                return CSVM\
                    .pop_jump_if_false(_instruction)
            case CSOpCode.POP_JUMP_IF_TRUE:
                return CSVM\
                    .pop_jump_if_true(_instruction)
            case CSOpCode.JUMP_IF_FALSE_OR_POP:
                return CSVM\
                    .jump_if_false_or_pop(_instruction)
            case CSOpCode.JUMP_IF_TRUE_OR_POP:
                return CSVM\
                    .jump_if_true_or_pop(_instruction)
            case CSOpCode.JUMP_EQUAL:
                return CSVM\
                    .jump_equal(_instruction)
            case CSOpCode.ABSOLUTE_JUMP:
                return CSVM\
                    .absolute_jump(_instruction)
            case CSOpCode.JUMP_TO:
                return CSVM\
                    .jump_to(_instruction)
            # =============== END ========

            # OK!!!
            case CSOpCode.SETUP_TRY:
                return CSVM\
                    .setup_try(_instruction)
            
            case CSOpCode.POP_TRY:
                return CSVM\
                    .pop_try(_instruction)

            # OK!!!
            case CSOpCode.PRINT_OBJECT:
                return CSVM\
                    .print_object(_instruction)
            
            # OK!!!
            case CSOpCode.NO_OPERATION:
                return CSVM\
                    .no_op(_instruction)

            # OK!!!
            case CSOpCode.POP_TOP:
                return CSVM\
                    .pop_top(_instruction)
            # OK!!!
            case CSOpCode.RETURN_OP:
                return CSVM\
                    .return_op(_instruction)
           
        raise NotImplementedError("opcode %s is not implemented!" % _instruction.opcode.name)
    

    # ================================== BEGIN EVAL METHODS|
    # =====================================================|

    @staticmethod
    def push_const(_instruction:Instruction):
        EvalStack.es_push(CSVM.VHEAP.allocate(_instruction.get("obj")))
    
    @staticmethod
    def push_name(_instruction:Instruction):
        EvalStack.es_push(CSVM.VHEAP.getAddress(_instruction.get("offset")))
    
    @staticmethod
    def push_local(_instruction:Instruction):
        EvalStack.es_push(CallStack.cs_peek_frame().getLocalAt(_instruction.get("offset")))
    
    @staticmethod
    def make_array(_instruction:Instruction):
        _size = _instruction.get("size")

        _array = CSObject.new_array()
        for idx in range(_size):
            _array.push(EvalStack.es_pop())
        
        EvalStack.es_push(_array)
    
    @staticmethod
    def make_object(_instruction:Instruction):
        _size = _instruction.get("size")

        _object = CSObject.new_map()

        for idx in range(_size):
            _k = EvalStack.es_pop()
            _v = EvalStack.es_pop()
            _object.put(_k.__str__(), _v)
        
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
        EvalStack.es_push(_top.getAttribute(_instruction.get("attr")))

    @staticmethod
    def set_attrib(_instruction:Instruction):
        _top = EvalStack.es_pop()
        _att = EvalStack.es_pop()
        _top.setAttribute(_instruction.get("attr"), _att)
        EvalStack.es_push(_att)
    
    @staticmethod
    def store_name(_instruction:Instruction):
        _value = EvalStack.es_peek()
        CSVM.VHEAP.setAddress(_instruction.get("offset"), _value.offset)
    
    @staticmethod
    def store_local(_instruction:Instruction):
        CSVM.cs_peek_frame().store_local(_instruction.get("offset"), EvalStack.es_pop())
    
    @staticmethod
    def call(_instruction:Instruction):
        _top = EvalStack.es_pop()
        EvalStack.es_push(_top.call(_instruction.get("location"), _instruction.get("size")))

    
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
        EvalStack.es_push(_lhs.mul(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_div(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.div(_instruction.get("opt"), _rhs))

    @staticmethod
    def binary_mod(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.mod(_instruction.get("opt"), _rhs))

    @staticmethod
    def binary_add(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.add(_instruction.get("opt"), _rhs))

    @staticmethod
    def binary_sub(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.sub(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_lshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.lshift(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_rshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.rshift(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_and(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.bit_and(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_xor(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.bit_xor(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_or(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.bit_or(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_subscript(_instruction:Instruction):
        _member = EvalStack.es_pop()
        _object = EvalStack.es_pop()
        EvalStack.es_push(_object.subscript(_instruction.get("location"), _member))
    
    @staticmethod
    def set_subscript(_instruction:Instruction):
        _member  = EvalStack.es_pop()
        _object  = EvalStack.es_pop()
        _new_val = EvalStack.es_pop()
        EvalStack.es_push(_object.subscriptSet(_instruction.get("location"), _member, _new_val))
    # ============================= END

    
    # ===================== COMPARE OP|
    # ================================|
    @staticmethod
    def compare_op(_instruction:Instruction):
        _opt = _instruction.get("opt")
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        
        match _opt.token:
            case "<":
                return EvalStack.es_push(_lhs.lt(_opt, _rhs))
            case "<=":
                return EvalStack.es_push(_lhs.lte(_opt, _rhs))
            case ">":
                return EvalStack.es_push(_lhs.gt(_opt, _rhs))
            case ">=":
                return EvalStack.es_push(_lhs.gte(_opt, _rhs))
            case "==":
                return EvalStack.es_push(_lhs.eq(_opt, _rhs))
            case "!=":
                return EvalStack.es_push(_lhs.neq(_opt, _rhs))
        # error operator
        raise ValueError("invalid or not implemented op \"%s\"" % _opt.token)
    # ============================= END



    # ===================== INPLACE OP|
    # ================================|
    @staticmethod
    def inplace_pow(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.pow(_instruction.get("opt"), _rhs))
    @staticmethod
    def inplace_mul(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.mul(_instruction.get("opt"), _rhs))
    @staticmethod
    def inplace_div(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.div(_instruction.get("opt"), _rhs))
    @staticmethod
    def inplace_add(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.add(_instruction.get("opt"), _rhs))
    @staticmethod
    def inplace_sub(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.sub(_instruction.get("opt"), _rhs))
    @staticmethod
    def inplace_lshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.lshift(_instruction.get("opt"), _rhs))
    @staticmethod
    def inplace_rshift(_instruction:Instruction):
        _lhs = EvalStack.es_pop()
        _rhs = EvalStack.es_pop()
        EvalStack.es_push(_lhs.rshift(_instruction.get("opt"), _rhs))
    # ============================= END



    # ======================== JUMP OP|
    # ================================|
    # NOTE: divide target by 2 to get the exact index
    @staticmethod
    def pop_jump_if_false(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_pop()

        if not (_top.get("this")):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)

    @staticmethod
    def pop_jump_if_true(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_pop()

        if _top.get("this"):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
    
    @staticmethod
    def jump_if_false_or_pop(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_peek()

        if not _top.get("this"):
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
            return

        EvalStack.es_pop()
    
    @staticmethod
    def jump_if_true_or_pop(_instruction:Instruction):
        _target = _instruction.get("target") // 2

        _top = EvalStack.es_peek()

        if _top.get("this"):
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

        if _lhs.equals(_rhs):
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
            _fmt += "%s" % EvalStack.es_pop().__str__()
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


