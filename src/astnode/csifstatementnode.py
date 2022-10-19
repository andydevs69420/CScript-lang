from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


# OK!!! | COMPILED | PASSED
class IfStatementNode(CSAst):

    def __init__(self, _condition:CSAst, _statement:CSAst, _else:CSAst):
        super().__init__()
        self.condition  = _condition
        self.statement  = _statement
        self.else_stmnt = _else

    def compile(self):
        _evaluated = self.condition.evaluate()
        if  _evaluated:
            if  _evaluated.getObject().get("this"):
                # condition met|true|satisfiable
                self.statement.compile()
            else:
                if  self.else_stmnt:
                    self.else_stmnt.compile()
            return
        
        # compile branching?
        if self.condition.isOverloading():
            self.logical()
        else:
            self.default()
    
    def logical(self):
        _jump_t0, _jump_t1 = None, None

        # extract rhs and compile
        _rhs_evaluated = self.condition.rhs.evaluate()
        _rhs_evaluated = _rhs_evaluated.getObject().get("this") if _rhs_evaluated else False

        if  not _rhs_evaluated:
            self.condition.rhs.compile()

            # check rhs
            if  self.condition.opt.matches("&&"):
                # logical and
                self.pop_jump_if_false(...)
            else:
                # logical or
                self.pop_jump_if_true(...)

            _jump_t0 = self.peekLast()
        
        _lhs_evaluated = self.condition.lhs.evaluate()
        _lhs_evaluated = _lhs_evaluated.getObject().get("this") if _lhs_evaluated else False

        if  not _lhs_evaluated:
            # extract lhs and compile
            self.condition.lhs.compile()

            # always pop jump if false lhs
            self.pop_jump_if_false(...)

            _jump_t1 = self.peekLast()

        # jump to this location if rhs is true when "logical or".
        # do not evaluate lhs
        if  self.condition.opt.matches("||"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = self.getLine()

        # statement
        self.statement.compile()

        self.jump_to(...)
        _jump_t2 = self.peekLast()

        # jump to this location if rhs is false when "logical and".
        # do not evaluate lhs
        if  self.condition.opt.matches("&&"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = self.getLine()

        if  not _lhs_evaluated:
            # set jump target 1
            _jump_t1.kwargs["target"] = self.getLine()

        # compile else
        if  self.else_stmnt:
            self.else_stmnt.compile()
        
        # set jump target 1
        _jump_t2.kwargs["target"] = self.getLine()


    def default(self):
        self.condition.compile()

        self.pop_jump_if_false(...)
        _jump_t0 = self.peekLast()
        
        # compile statement
        self.statement.compile()

        self.jump_to(...)
        _jump_t1 = self.peekLast()

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

        # compile else
        if  self.else_stmnt:
            self.else_stmnt.compile()
        
        # set jump target 1
        _jump_t1.kwargs["target"] = self.getLine()
