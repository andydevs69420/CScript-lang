
from object.csobject import CSObject
from .compilable import Instruction
from .csOpcode import CSOpCode

class ExceptionTable:

    @staticmethod
    def make(_id:int, ):
        ...



class EvalStack:
    """ Evaluation stack for CSCript
    """
    
    EVAL_STACK = [
        # +------------+ ^
        # | CSObject N | |
        # +------------+ |
        #                |
        # +------------+ |
        # | CSObject 0 | |
        # +------------+ |
    ]

    @staticmethod
    def push(_object:CSObject):
        return EvalStack.EVAL_STACK\
            .append(_object)
    
    @staticmethod
    def peek():
        return EvalStack.EVAL_STACK[-1]

    @staticmethod    
    def pop():
        return EvalStack.EVAL_STACK\
            .pop()
    
    @staticmethod
    def isEmpty():
        return len(EvalStack.EVAL_STACK) <= 0


class Frame(object):

    def __init__(self, _instructions:list[Instruction]):
        self.returned = False
        self.ipointer = 0
        self.locals = []
        self.instructions = _instructions

    def next(self):
        _code = self.instructions[self.ipointer]
        self.ipointer += 1
        return _code
    
    def setReturn(self, _returned:bool):
        self.returned = _returned

    def isReturned(self):
        return self.returned or self.ipointer >= len(self.instructions)


class CallStack:
    
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
    def hasFrame():
        return len(CallStack.CALL_STACK) > 0

    @staticmethod
    def push_frame(_instruction:list[Instruction]):
        CallStack.CALL_STACK\
        .append(
            Frame(_instruction)
        )
    
    @staticmethod
    def peek_frame():
        return CallStack.CALL_STACK[-1]
    
    @staticmethod
    def pop_frame():
        return CallStack.CALL_STACK.pop()





class Memory:

    MEM:list[CSObject] = [
        # object
    ]

    REF:dict = ({
        # [offset|index] : count
    })

    @staticmethod
    def incRef(_offset:int):
        Memory.REF[_offset] += 1
    
    @staticmethod
    def decRef(_offset:int):
        Memory.REF[_offset] -= 1

        # delete|Set None if zero
        if  Memory.REF[_offset] <= 0:
            Memory.MEM[_offset]  = None
            print("DELETED: %d" % _offset)

    @staticmethod
    def makeSlot():
        # make slot
        _idx = len(Memory.MEM)
        Memory.MEM.append(CSObject.new_nulltype("null"))

        # add initial ref count
        Memory.REF[_idx] = 1

        return _idx
    
    @staticmethod
    def memGet(_offset:int):
        return Memory.MEM[_offset]
    
    @staticmethod
    def memSet(_offset:int, _obj:CSObject):
        Memory.MEM[_offset] = _obj


class CSVirtualMachine(
    ExceptionTable, 
    EvalStack     , 
    CallStack     ,
    Memory        ,
):
    
    @staticmethod
    def run(_instruction:list[Instruction]):
        CallStack.push_frame(_instruction)

        # run
        while CallStack.hasFrame():
            
            _top:Frame = CallStack.peek_frame()

            while not _top.isReturned():
                _bcode = _top.next()
                CSVirtualMachine.evaluate(_bcode)
            
            # pop if done
            CallStack.pop_frame()
    
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

            case CSOpCode.MAKE_CLASS:
                return CSVirtualMachine\
                    .make_class(_instruction)
            case CSOpCode.MAKE_MODULE:
                return CSVirtualMachine\
                    .make_module(_instruction)
            
            # OK!!!
            case CSOpCode.STORE_NAME:
                return CSVirtualMachine\
                    .store_name(_instruction)
            
            # ================ UNARY EXPR
            # ===========================
            case CSOpCode.UNARY_OP:
                return CSVirtualMachine\
                    .unary_op(_instruction)
            # =============== END =======


            # OK!!!
            # =============== BINARY EXPR
            # ===========================
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
            # =============== END =======

            # OK!!!
            case CSOpCode.POP_TOP:
                return CSVirtualMachine\
                    .pop_top(_instruction)
            # OK!!!
            case CSOpCode.RETURN_OP:
                return CSVirtualMachine\
                    .return_op(_instruction)
           
        raise NotImplementedError("opcode %s is not implemented!" % _instruction.opcode.name)
    
    @staticmethod
    def push_const(_instruction:Instruction):
        EvalStack.push(_instruction.get("obj"))
    
    @staticmethod
    def push_name(_instruction:Instruction):
        EvalStack.push(Memory.memGet(_instruction.get("offset")))
    
    @staticmethod
    def make_class(_instruction:Instruction):
        print(_instruction)

    @staticmethod
    def make_module(_instruction:Instruction):
        # _module = CSObject()

        # while not EvalStack.isEmpty():
        #     _name  = EvalStack.pop()
        #     _value = EvalStack.pop()
        #     _module.put(_name.get("this").__str__(), _value)
        
        # EvalStack.push(_module)
        ...
    
    @staticmethod
    def store_name(_instruction:Instruction):
        _val = EvalStack.pop()
        Memory.memSet(_instruction.get("offset"), _val)
    
    # ================ UNARY OPERATION
    # ================================
    @staticmethod
    def unary_op(_instruction:Instruction):
        _opt = _instruction.get("opt")
        _rhs = EvalStack.pop()
        match _opt.token:
            case "~":
                return EvalStack.push(_rhs.bit_not(_opt))
            case "!":
                return EvalStack.push(_rhs.binary_not(_opt))
            case "+":
                return EvalStack.push(_rhs.positive(_opt))
            case "-":
                return EvalStack.push(_rhs.negative(_opt))
        # error operator
        raise ValueError("invalid or not implemented op \"%s\"" % _opt.token)
    # ============================ END
    

    # =============== BINARY OPERATION
    # ================================
    
    @staticmethod
    def binary_mul(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.mul(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_div(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.div(_instruction.get("opt"), _rhs))

    @staticmethod
    def binary_mod(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.mod(_instruction.get("opt"), _rhs))

    @staticmethod
    def binary_add(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.add(_instruction.get("opt"), _rhs))

    @staticmethod
    def binary_sub(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.sub(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_lshift(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.lshift(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_rshift(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.rshift(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_and(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.bit_and(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_xor(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.bit_xor(_instruction.get("opt"), _rhs))
    
    @staticmethod
    def binary_or(_instruction:Instruction):
        _lhs = EvalStack.pop()
        _rhs = EvalStack.pop()
        EvalStack.push(_lhs.bit_or(_instruction.get("opt"), _rhs))
    # ============================ END



    @staticmethod
    def pop_top(_instruction:Instruction):
        EvalStack.pop()

    @staticmethod
    def return_op(_instruction:Instruction):
        CallStack.peek_frame().setReturn(True)


