



from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import  CodeBlock


class BreakNode(CSAst):
    """ Handles break statement
    """
    def __init__(self):
        super().__init__()
    
    def compile(self, _block:CodeBlock):
        
        # add initial jump instruction
        _block.jump_to(...)
        _jump_t0 = _block.peekLast()

        # push to break__stack
        _block.break__stack.append(_jump_t0)

        # let loop handles jump to current control

    def isBreak(self):
        return True
