from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock

# OK!!! | COMPILED | PASSED
class SwitchNode(CSAst):
    """ Holds switch statement

        Parameters
        ----------
        _condition : CSAst
        _body      : dict
    """

    def __init__(self, _condition:CSAst, _body:dict):
        super().__init__()
        self.condition = _condition
        self.body = _body

    def compile(self, _block:CodeBlock):
        _jump_end = []
        
        for case in self.body["cases"]:

            _jump_to_stmnt = []

            for match in case["case"]:
                # compile current match
                match.compile(_block)
                
                # compile condition
                self.condition.compile(_block)

                _block.jump_equal(...)
                _jump_to_stmnt.append(_block.peekLast())
            
            _block.absolute_jump(...)
            _jump_next = _block.peekLast()
            
            # jump here if matches
            for matched in _jump_to_stmnt:
                matched.kwargs["target"] = _block.getLine()

            # case statement
            case["stmnt"].compile(_block)

            _block.jump_to(...)
            _jump_end.append(_block.peekLast())

            # jump to next case|else
            _jump_next.kwargs["target"] = _block.getLine()
        
        if  self.body["else"]:
            self.body["else"].compile(_block)
        
        for _jump in _jump_end:
            _jump.kwargs["target"] = _block.getLine()
