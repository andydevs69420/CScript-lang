from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable


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
        if  _props["_global"]:
            self.push_name(self.reference, _props["_slot"])
        else:
            self.push_local(self.reference, _props["_slot"])

    
    def assignTo(self):
        self.assertExists()
        _props = ST.lookup(self.reference.token)

        # ============ COMPILE|
        # ====================|
        # compile
        if  _props["_global"]:
            self.store_name(self.reference, _props["_slot"])
        else:
            self.store_local(self.reference, _props["_slot"])


        # push to stack new value
        self.compile()
    
    def isAssignable(self):
        return True