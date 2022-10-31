from astnode.globalast.csAst import CSAst, CSToken,  ST
from astnode.globalast.cscodeblock import CodeBlock

class TryExceptNode(CSAst):

    def __init__(self, _try_body:CSAst, _execpt_param:CSToken, _except_body:CSAst, _finally_body:CSAst|None):
        super().__init__()
        self.try_body = _try_body
        self.except_param = _execpt_param
        self.except_body = _except_body
        self.finally_body = _finally_body
    
    def compile(self, _block:CodeBlock):
        # setup try/except jump if error
        _block.setup_try(...)
        _will_jump_to = _block.peekLast()

        # compile body
        self.try_body.compile(_block)

        # add jump to finally(if any) | end try/except
        _block.jump_to(...)
        _jump_t0 = _block.peekLast()

        _block.symbtable.newScope()

        _s = _block.newlocals()

        _block.symbtable.current.insert(self.except_param.token, _slot=_s, _global=False)

        # record jump location  if error
        _will_jump_to.kwargs["target"] = _block.getLine()

        # pop try/except block
        _block.pop_try()

        _block.store_local(self.except_param, _s)

        # compile except
        self.except_body.compile(_block)
        # automatically goto finally (if any).
        # without jump

        _block.symbtable.endScope()

        # set jump target 0
        _jump_t0.kwargs["target"] = _block.getLine()

        # compile finally
        if  self.finally_body:
            self.finally_body.compile(_block)
