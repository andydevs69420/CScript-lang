from csAst import CSToken, CSAst, CSObject, show_error, ST, VM, Evaluator, Evaluatable

class LetNode(CSAst):
    """ Holds let declairation

        Parameters
        ----------
        _assignments : tuple
    """

    def __init__(self, _assignments:tuple):
        super().__init__()
        self.assignments = _assignments
    
    def compile(self):
        for assignment in self.assignments:
            # compile value
            if  not assignment["val"]:
                # unstable | not appropriate
                _null = CSObject.new_nulltype("null")
                _null.cleanLast()

                self.push_constant(_null)
            else:
                assignment["val"].compile()
            

            _var = assignment["var"]

            # ================= RECORDING PURPOSE|
            # ===================================|
            # check existence
            if  ST.islocal(_var.token):
                return show_error("local variable \"%s\" is already defined" % _var.token, _var)
            
            # possible ok!
            _s = self.newlocal()

            # save var_name
            ST.insert(_var.token, _slot=_s, _global=True)

            # ============ MEMORY SETTING PURPOSE|
            # ===================================|
            # store name
            self.store_name(_var, _s)


