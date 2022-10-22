from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock


# OK!!! | COMPILED | PASSED
class WhileNode(CSAst):
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
    
    def compile(self, _block:CodeBlock):
        _evaluated = self.condition.evaluate()
        if  _evaluated:
            if  not _evaluated.getObject().get("this"):
                # false condition|no operation
                self.no_operation()
                return

        # compile
        if  self.condition.islogical():
            self.logical(_block)
        else:
            self.default(_block)
    
    def logical(self, _block:CodeBlock):
        _jump_t0, _jump_t1 = None, None

        _begin = _block.getLine()
        
        _rhs_evaluated = self.condition.rhs.evaluate()
        _rhs_evaluated = _rhs_evaluated.get("this") if _rhs_evaluated else False

        if  not _rhs_evaluated:
            # compile rhs
            self.condition.rhs.compile(_block)

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
            # compile rhs
            self.condition.lhs.compile(_block)
            
            # always pop jump if false lhs
            _block.pop_jump_if_false(...)
            
            _jump_t1 = _block.peekLast()


        # # jump to this location if rhs is true when "logical or"!
        if  self.condition.opt.matches("||"):
            # set jump target 0
            _jump_t0.kwargs["target"] = _block.getLine()

        # compile body
        self.body.compile(_block)

        # jumpt to condition
        _block.absolute_jump(_begin)

        # jump to this|end location if rhs is false when "logical and"!
        # do not evaluate lhs
        if  self.condition.opt.matches("&&"):
            if  not _rhs_evaluated:
                # set jump target 0
                _jump_t0.kwargs["target"] = _block.getLine()
        
        if  not _lhs_evaluated:
            # set jump target 0
            _jump_t1.kwargs["target"] = _block.getLine()
    
    def default(self, _block:CodeBlock):
        _begin = _block.getLine()

        # compile condition
        self.condition.compile(_block)

        _block.pop_jump_if_false(...)
        _jump_t0 = _block.peekLast()

        # compile body
        self.body.compile(_block)

        # jump to condition
        _block.absolute_jump(_begin)

        # set jump target 0
        _jump_t0.kwargs["target"] = _block.getLine()
