""" Ast interfaces that produces code blocks
"""


from .csAst import ST, CSAst


class CodeBlock(CSAst):
    def __init__(self):
        super().__init__()
        self.symbtable:ST = ST()
        self.__locals:int = 0
        self.__globals:int = 0

        # used in continue
        self.loop__stack = [
            # while N
            # ...
            # while 0
        ]

        # used in loop
        """ Example

            code:
            
            while (cond)
            {
                break;
            }

            # implement:
                jump_here = pop(break_stack)
                jump_here.target = currentLine;

        """
        self.break__stack = [
            # break N
            # ...
            # break 0
        ]
    
    def newlocals(self):
        _old = self.__locals
        self.__locals += 1
        return _old
    
    def newglobals(self):
        _old = self.__globals
        self.__globals += 1
        return _old
    
    def getlocals(self):
        return self.__locals
    
    def getglobals(self):
        return self.__globals
