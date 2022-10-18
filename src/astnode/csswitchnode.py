
from csAst import CSAst


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

    def compile(self):
        _jump_end = []
        
        for case in self.body["cases"]:

            _jump_to_stmnt = []

            for match in case["case"]:
                # compile current match
                match.compile()
                
                # compile condition
                self.condition.compile()

                self.jump_equal(...)
                _jump_to_stmnt.append(self.peekLast())
            
            self.absolute_jump(...)
            _jump_next = self.peekLast()
            
            # jump here if matches
            for matched in _jump_to_stmnt:
                matched.kwargs["target"] = self.getLine()

            # case statement
            case["stmnt"].compile()

            self.jump_to(...)
            _jump_end.append(self.peekLast())

            # jump to next case|else
            _jump_next.kwargs["target"] = self.getLine()
        
        if  self.body["else"]:
            self.body["else"].compile()
        
        for _jump in _jump_end:
            _jump.kwargs["target"] = self.getLine()
