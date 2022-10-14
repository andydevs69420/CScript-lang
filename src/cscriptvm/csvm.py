
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


class CSVirtualMachine(
    ExceptionTable, 
    EvalStack     , 
    CallStack     ,
):
    
    MEM:CSObject = [
        # object
    ]

    

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
            case CSOpCode.PUSH_CONST:
                return CSVirtualMachine\
                    .push_const(_instruction)
            case CSOpCode.MAKE_CLASS:
                return CSVirtualMachine\
                    .make_class(_instruction)
            case CSOpCode.MAKE_MODULE:
                return CSVirtualMachine\
                    .make_module(_instruction)
            case CSOpCode.POP_TOP:
                return CSVirtualMachine\
                    .pop_top(_instruction)
            case CSOpCode.RETURN_OP:
                return CSVirtualMachine\
                    .return_op(_instruction)
           
        raise NotImplementedError("opcode %s is not implemented!" % _instruction.opcode.name)
    
    @staticmethod
    def push_const(_instruction:Instruction):
        EvalStack.push(_instruction.get("obj"))
    
    @staticmethod
    def make_class(_instruction:Instruction):
        print(_instruction)

    @staticmethod
    def make_module(_instruction:Instruction):
        _module = CSObject()

        while not EvalStack.isEmpty():
            _name  = EvalStack.pop()
            _value = EvalStack.pop()
            _module.put(_name.get("this"), _value)
        
        EvalStack.push(_module)
    
    @staticmethod
    def pop_top(_instruction:Instruction):
        EvalStack.pop()

    @staticmethod
    def return_op(_instruction:Instruction):
        print(EvalStack.peek())
        CallStack.peek_frame().setReturn(True)


