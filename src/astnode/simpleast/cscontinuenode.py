



from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock


class ContinueNode(CSAst):

    def __init__(self):
        super().__init__()
    
    def compile(self, _block:CodeBlock):
        # jump to  nearest "loop" start
        _block.absolute_jump(_block.loop__stack[-1])
    
    def isContinue(self):
        return True

