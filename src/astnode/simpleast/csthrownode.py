

from astnode.globalast.csAst import CSAst
from astnode.globalast.cscodeblock import CodeBlock
from cstoken import CSToken


class ThrowNode(CSAst):
    """
    """

    def __init__(self, _exception:CSAst, _loc:CSToken):
        self.exception = _exception
        self.location  = _loc
    
    def compile(self, _block:CodeBlock):
        # compile exception
        self.exception.compile(_block)

        # calls throw_error on vm
        _block.throw_error(self.location)

