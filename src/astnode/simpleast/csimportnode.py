



from astnode.globalast.csAst import CSToken, CSAst
from astnode.globalast.cscodeblock import CodeBlock


class ImportNode(CSAst):
    """
    """

    def __init__(self, _imports:tuple, _source:CSAst, _location:CSToken):
        super().__init__()
        self.imports  = _imports
        self.source   = _source
        self.location = _location
    
    def compile(self, _block:CodeBlock):
        # push source
        self.source.compile(_block)

        _block.load_module()

        for each_import in self.imports:
            # get module attribute
            _block.load_attrib(each_import)

            _s = _block.newglobals()

            # save as global var
            _block.symbtable.current.insert(each_import.token, _slot=_s, _global=True, _token=each_import)

            # create reference
            _block.store_name(each_import, _s)

        # pop module
        _block.pop_top()
