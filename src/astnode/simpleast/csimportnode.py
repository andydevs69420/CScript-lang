



from astnode.globalast.csAst import CSToken, CSAst
from astnode.globalast.cscodeblock import CodeBlock

from cshelpers import __trim__

class ImportNode(CSAst):
    """
    """

    def __init__(self, _source:CSAst, _location:CSToken):
        super().__init__()
        self.source   = _source
        self.location = _location
    
    def compile(self, _block:CodeBlock):
        # push source | string node by default
        self.source.compile(_block)

        _block.load_module(self.location)

        _s = _block.newglobals()

        # 
        _name = __trim__(self.source.evaluate().__str__())
        print(_name)

        _block.symbtable.current.insert(_name, _slot=_s, _global=True, _token=self.source.string)

        _block.store_name(self.source.string, _s)