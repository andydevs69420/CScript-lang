from astnode.globalast.csAst import CSToken, show_error
from astnode.globalast.cscodeblock import CodeBlock
from astnode.globalast.csexprast import ExpressionAst


class ReferenceNode(ExpressionAst):
    """ Holds reference

        Parameters
        ----------
        _id : CSToken
    """

    def __init__(self, _id:CSToken):
        super().__init__()
        self.reference = _id
    
    def assertExists(self, _block:CodeBlock):
        # check if exists
        if  not _block.symbtable.current.existsglobally(self.reference.token):
            return show_error("name \"%s\" is not defined" % self.reference.token, self.reference)
   
    def compile(self, _block:CodeBlock):
        self.assertExists(_block)
        _props = _block.symbtable.current.lookup(self.reference.token)

        # compile
        if  _props["_global"]:
            _block.push_name(self.reference, _props["_slot"])
        else:
            _block.push_local(self.reference, _props["_slot"])

    
    def assignTo(self, _block:CodeBlock, _opt:CSToken):
        self.assertExists(_block)
        _props = _block.symbtable.current.lookup(self.reference.token)

        # ============ COMPILE|
        # ====================|
        # compile
        if  _props["_global"]:
            _block.store_name(self.reference, _props["_slot"])
        else:
            _block.store_local(self.reference, _props["_slot"])


        # push to stack new value
        self.compile(_block)