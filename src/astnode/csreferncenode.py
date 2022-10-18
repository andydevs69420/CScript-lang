
from cstoken import CSToken
from csAst import CSAst
from errortoken import show_error

# core
from cscriptvm.csvm import CSVirtualMachine as VM
from cscriptvm.cssymboltable import CSSymbolTable as ST



class ReferenceNode(CSAst):
    """ Holds reference

        Parameters
        ----------
        _id : CSToken
    """

    def __init__(self, _id:CSToken):
        super().__init__()
        self.reference = _id
    
    def assertExists(self):
        # check if exists
        if  not ST.exists(self.reference.token):
            return show_error("name \"%s\" is not defined" % self.reference.token, self.reference)
   
    def compile(self):
        self.assertExists()
        _props = ST.lookup(self.reference.token)

        # compile
        self.push_name(self.reference, _props["_slot"])

    
    def assignTo(self):
        self.assertExists()
        _props = ST.lookup(self.reference.token)

        # ============ COMPILE|
        # ====================|
        # compile
        self.store_name(self.reference, _props["_slot"])


        # push to stack new value
        self.push_name (self.reference, _props["_slot"])
    
    def isAssignable(self):
        return True