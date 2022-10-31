
from astnode.utils.compilable import Instruction

# ======= object|
# ==============|
from base.csobject import CSObject
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

    @staticmethod
    def isrunning():
        return EvalStack.es_isEmpty()

    @staticmethod
    def run(_instruction:list[Instruction]):

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
        
        return _top
    
    @staticmethod
    def throw_error(_csobject:CSObject):
        from cshelpers import __throw__
        if  not ExceptionTable.et_is_empty():
            # if exception table is not empty,
            # jump to whats being returned
            _target = ExceptionTable.et_peek() // 2
            CallStack\
                .cs_peek_frame()\
                    .setPointer(_target)
        else:
            # TODO: replace with cscript stderr
            return __throw__(_csobject.__str__())
    
    # ==================================== OPCODE EVALUATOR|
    # =====================================================|
    @staticmethod
    def evaluate(_instruction:Instruction):
        match _instruction.opcode:
            
            case CSOpCode.BINARY_ADD:
                ...
            case _:
                raise NotImplementedError()