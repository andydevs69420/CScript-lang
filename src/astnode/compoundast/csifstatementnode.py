from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock


# OK!!! | COMPILED | PASSED
class IfStatementNode(CSAst):

    def __init__(self, _condition:CSAst, _statement:CSAst, _else:CSAst):
        super().__init__()
        self.condition  = _condition
        self.statement  = _statement
        self.else_stmnt = _else

    def compile(self, _block:CodeBlock):
        _evaluated = self.condition.evaluate()
        if  _evaluated:
            if  _evaluated.get("this"):
                # condition met|true|satisfiable
                self.statement.compile(_block)
            else:
                if  self.else_stmnt:
                    self.else_stmnt.compile(_block)
            return
        
        # compile branching?
        if self.condition.islogical():
            self.logical(_block)
        else:
            self.default(_block)
    
    def logical(self, _block:CodeBlock):
        _jump_t0, _jump_t1 = None, None

        # extract rhs and compile
        _rhs_evaluated = self.condition.rhs.evaluate()
        _rhs_evaluated = _rhs_evaluated.get("this") if _rhs_evaluated else False

        if  not _rhs_evaluated:
            self.condition.rhs.compile(_block)

            # check rhs
            if  self.condition.opt.matches("&&"):
                # logical and
                _block.pop_jump_if_false(...)
            else:
                # logical or
                _block.pop_jump_if_true(...)

            _jump_t0 = _block.peekLast()
        
        _lhs_evaluated = self.condition.lhs.evaluate()
        _lhs_evaluated = _lhs_evaluated.get("this") if _lhs_evaluated else False

        if  not _lhs_evaluated:
            # extract lhs and compile
            self.condition.lhs.compile(_block)

            # always pop jump if false lhs
            _block.pop_jump_if_false(...)

            _jump_t1 = _block.peekLast()

        # jump to this location if rhs is true when "logical or".
        # do not evaluate lhs
        if  self.condition.opt.matches("||"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = _block.getLine()

        # statement
        self.statement.compile(_block)

        _block.jump_to(...)
        _jump_t2 = _block.peekLast()

        # jump to this location if rhs is false when "logical and".
        # do not evaluate lhs
        if  self.condition.opt.matches("&&"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = _block.getLine()

        if  not _lhs_evaluated:
            # set jump target 1
            _jump_t1.kwargs["target"] = _block.getLine()

        # compile else
        if  self.else_stmnt:
            self.else_stmnt.compile(_block)
        
        # set jump target 1
        _jump_t2.kwargs["target"] = _block.getLine()


    def default(self, _block:CodeBlock):
        self.condition.compile(_block)

        _block.pop_jump_if_false(...)
        _jump_t0 = _block.peekLast()
        
        # compile statement
        self.statement.compile(_block)

        _block.jump_to(...)
        _jump_t1 = _block.peekLast()

        # set jump target 0
        _jump_t0.kwargs["target"] = _block.getLine()

        # compile else
        if  self.else_stmnt:
            self.else_stmnt.compile(_block)
        
        # set jump target 1
        _jump_t1.kwargs["target"] = _block.getLine()
