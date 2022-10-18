from csAst import CSAst


# OK!!! | COMPILED | PASSED
class DoWhileNode(CSAst):
    """ Holds while statement

        Parameters
        ----------
        _condition : CSAst
        _body      : CSAst
    """

    def __init__(self, _condition:CSAst, _body:CSAst):
        super().__init__()
        self.condition = _condition
        self.body = _body
    
    def compile(self):
        _evaluated = self.condition.evaluate()
        if  _evaluated:
            if  not _evaluated.get("this"):
                # false condition|no operation
                self.no_operation()
                return

        # compile
        if  self.condition.isOverloading():
            self.logical()
        else:
            self.default()

    
    def logical(self):
        _jump_t0, _jump_t1 = None, None

        _begin = self.getLine()

        # compile body
        self.body.compile()
        
        _rhs_evaluated = self.condition.rhs.evaluate()
        _rhs_evaluated = _rhs_evaluated.get("this") if _rhs_evaluated else False

        if  not _rhs_evaluated:
            # compile rhs
            self.condition.rhs.compile()

            if  self.condition.opt.matches("&&"):
                # logical and
                self.pop_jump_if_false(...)
            else:
                # logical or
                self.pop_jump_if_true(...)
            
            _jump_t0 = self.peekLast()

        _lhs_evaluated = self.condition.lhs.evaluate()
        _lhs_evaluated = _lhs_evaluated.get("this") if _lhs_evaluated else False

        if  not _lhs_evaluated:
            # compile rhs
            self.condition.lhs.compile()
            
            # always pop jump if false lhs
            self.pop_jump_if_false(...)
            
            _jump_t1 = self.peekLast()


        # # jump to this location if rhs is true when "logical or"!
        if  self.condition.opt.matches("||"):
            # set jump target 0
            _jump_t0.kwargs["target"] = self.getLine()

        # jumpt to condition
        self.absolute_jump(_begin)

        # jump to this|end location if rhs is false when "logical and"!
        # do not evaluate lhs
        if  self.condition.opt.matches("&&"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = self.getLine()
        
        if  not _lhs_evaluated:
            # set jump target 0
            _jump_t1.kwargs["target"] = self.getLine()

    def default(self):
        _begin = self.getLine()

        # compile body
        self.body.compile()

        # compile condition
        self.condition.compile()

        self.pop_jump_if_false(...)
        _jump_t0 = self.peekLast()

        # jump to condition
        self.absolute_jump(_begin)

        # set jump target 0
        _jump_t0.kwargs["target"] = self.getLine()

