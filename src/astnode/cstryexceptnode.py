from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

class TryExceptNode(CSAst):

    def __init__(self, _try_body:CSAst, _execpt_param:CSToken, _except_body:CSAst, _finally_body:CSAst|None):
        super().__init__()
        self.try_body = _try_body
        self.except_param = _execpt_param
        self.except_body = _except_body
        self.finally_body = _finally_body
    
    def compile(self):
        # setup try/except jump if error
        self.setup_try(...)
        _will_jump_to = self.peekLast()

        # compile body
        self.try_body.compile()

        # add jump to finally(if any) | end try/except
        self.jump_to(...)
        _jump_t0 = self.peekLast()

        ST.newScope()

        _s = VM.makeSlot()

        ST.insert(self.except_param.token, _slot=_s, _global=True)

        # record jump location  if error
        _will_jump_to.kwargs["target"] = self.getLine()

        self.store_name(self.except_param, _s)

        # compile except
        self.except_body.compile()
        # automatically goto finally (if any).
        # without jump

        ST.endScope()

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

        # compile finally
        if  self.finally_body:
            self.finally_body.compile()

        # pop try/except block
        self.pop_try()


