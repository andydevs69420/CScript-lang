""" Ast interfaces that produces code blocks
"""


from .csAst import ST, CSAst


class CodeBlock(CSAst):
    def __init__(self):
        super().__init__()
        self.symbtable:ST = ST()
        self.__locals:int = 0
        self.__globals:int = 0
    
    def newlocals(self):
        _old = self.__locals
        self.__locals += 1
        return _old
    
    def newglobals(self):
        _old = self.__globals
        self.__globals += 1
        return _old
