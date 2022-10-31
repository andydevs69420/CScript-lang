from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst
from astnode.globalast.csAst import CSObject

# OK!!! | COMPILED | PASSED
class ObjectNode(ExpressionAst):
    """ Holds object node

        Parameters
        ----------
        _elements : tuple
    """

    def __init__(self, _elements:tuple):
        super().__init__()
        self.elements = _elements

    def compile(self, _block:CodeBlock):
        # compile right most first!
        for node in self.elements[::-1]:

            # value
            _evaluated = node["val"].evaluate()
            if  _evaluated:
                _block.push_constant(_evaluated)
            else:
                node["val"].compile(_block)
            
            # key|attrib
            _block.push_constant(CSObject.new_string(node["key"].token))

        # object opcode
        _block.make_object(len(self.elements))
