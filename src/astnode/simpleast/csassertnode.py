




from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock
from cstoken import CSToken


class AssertNode(CSAst):
    """
    """
    
    def __init__(self, _condition:CSAst, _message:CSAst, _loc:CSToken):
        super().__init__()
        self.condition = _condition
        self.message   = _message
        self.location  = _loc
    
    def compile(self, _block:CodeBlock):
        _condition = self.condition.evaluate()
        if  _condition:
            if  _condition.python():
                _block.no_operation()
                return
        
        # compile
        self.condition.compile(_block)

        # continue if true
        _block.pop_jump_if_true(...)
        _jump_t0 = _block.peekLast()
        
        # compile message
        self.message.compile(_block)

        # add throw
        _block.throw_error(self.location)

        # set jump target 0
        _jump_t0.kwargs["target"] = _block.getLine()


